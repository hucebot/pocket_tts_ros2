# ros2_kyutai_tts

A ROS 2 wrapper for [Kyutai Pocket TTS](https://github.com/kyutai-labs/pocket-tts). This node listens for text strings and publishes raw 16-bit PCM audio directly to the robot's speaker pipeline (e.g., TIAGo), bypassing the default text-to-speech engine.

## Requirements
* Docker
* Docker Compose
* Make

## Quick Start

1. Build the Docker container:
   ```bash
   make build
    ```

2. Run the node:
    ```bash
    make run
    ```



## ROS 2 API

### Subscriptions
* `/tts_input` (`std_msgs/msg/String`)
  Send text here to trigger speech generation.

### Publishers
* `/audio_out/raw` (`audio_common_msgs/msg/AudioData`)
  Raw 16-bit PCM audio bytes consumed by the robot's `audio_play` node.

## Usage Example

Publish a string to the input topic to hear the robot speak:
```bash
ros2 topic pub /tts_input std_msgs/msg/String "{data: 'Hello, I am using the Kyutai pocket text to speech engine.'}" -1
```

## Configuration (Changing Voices)

The default voice is set to `alba`. This is a built-in catalog voice that does not require a HuggingFace authentication token.

To change the voice, edit `ros2_kyutai_tts/kyutai_tts_node.py` and modify the prompt:

```python
self.voice_state = self.model.get_state_for_audio_prompt("marius")
```

**Available built-in voices:**
`cosette`, `marius`, `javert`, `alba`, `jean`, `anna`, `vera`, `fantine`, `charles`, `paul`, `eponine`, `azelma`, `george`, `mary`, `jane`, `michael`, `eve`, `bill_boerst`, `peter_yearsley`, `stuart_bell`, `caro_davy`, `giovanni`, `lola`, `juergen`, `rafael`, `estelle`.



