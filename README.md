# LocalTTS
An implementation of a local TTS using [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) and [Kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx)

## Dependencies
Follow the instructions in [Kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) to install onnxruntime-gpu. GPU usage is recommended to experience the best performance.

## Usage
The dependencies of this repository can be installed using [uv](https://github.com/astral-sh/uv), a Python package and project manager. The required Python version, dependencies, and uv.lock file are already present in the project. 

### Kokoro files
Two files are required to run to run kokoro: the model itself and the voice definition.
- Download Kokoro model in project folder
    - [Kokoro model](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx)
- Download Kokoro voices in project folder
    - [Kokoro voice](https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin)

For more information about the files, check the [releases](https://github.com/thewh1teagle/kokoro-onnx/releases).

## License
MIT 2025