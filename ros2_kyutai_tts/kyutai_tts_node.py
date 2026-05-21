#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData
from rcl_interfaces.msg import SetParametersResult
import numpy as np
import torch
from pocket_tts import TTSModel

class KyutaiTTSNode(Node):
    def __init__(self):
        super().__init__('kyutai_tts_node')

        # 1. Initialize and load the Pocket TTS model
        self.get_logger().info('Loading Kyutai Pocket TTS model (this may take a moment)...')
        self.model = TTSModel.load_model(language="english")

        # 2. Declare and load the initial voice parameter
        self.declare_parameter('voice', 'alba')
        initial_voice = self.get_parameter('voice').value

        try:
            self.voice_state = self.model.get_state_for_audio_prompt(initial_voice)
            self.get_logger().info(f'Successfully loaded default voice: {initial_voice}')
        except Exception as e:
            self.get_logger().error(f'Failed to load initial voice "{initial_voice}": {e}')
            # Fallback to alba if the user passed an invalid parameter on launch
            self.voice_state = self.model.get_state_for_audio_prompt("alba")

        self.get_logger().info(f'Model loaded. Sample rate: {self.model.sample_rate} Hz')

        # Register the callback to handle parameter changes at runtime
        self.add_on_set_parameters_callback(self.on_parameter_change)

        # 3. ROS interfaces
        self.text_sub = self.create_subscription(
            String,
            '/tts_input',
            self.text_callback,
            10
        )

        self.audio_pub = self.create_publisher(
            AudioData,
            '/audio_out/raw',
            10
        )

        self.get_logger().info('Kyutai TTS Node fully initialized and ready.')

    def on_parameter_change(self, params):
        for param in params:
            if param.name == 'voice':
                new_voice = param.value
                self.get_logger().info(f'Attempting to change voice to: "{new_voice}"')
                try:
                    # Update the voice state
                    self.voice_state = self.model.get_state_for_audio_prompt(new_voice)
                    self.get_logger().info(f'Successfully changed voice to: "{new_voice}"')
                except Exception as e:
                    self.get_logger().error(f'Failed to load voice "{new_voice}": {e}')
                    # Return unsuccessful so the parameter reverts to its previous valid state
                    return SetParametersResult(successful=False, reason=str(e))

        return SetParametersResult(successful=True)

    def text_callback(self, msg):
        if not msg.data.strip():
            return

        self.get_logger().info(f'Generating audio for: "{msg.data}"')

        try:
            # Generate the audio tensor [samples]
            audio_tensor = self.model.generate_audio(self.voice_state, msg.data)

            # Convert float32 tensor (-1.0 to 1.0) to 1.0 signed 16-bit PCM numpy array
            audio_np = audio_tensor.numpy()
            audio_int16 = (audio_np * 32767).astype(np.int16)

            # Convert to raw bytes
            raw_audio_bytes = audio_int16.tobytes()

            # Publish to the audio pipeline
            audio_msg = AudioData()
            audio_msg.data = list(raw_audio_bytes)
            self.audio_pub.publish(audio_msg)
            self.get_logger().info('Audio successfully published.')

        except Exception as e:
            self.get_logger().error(f'Failed to generate TTS: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = KyutaiTTSNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()