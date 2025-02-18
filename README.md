## LLM Sandbox

**Lightweight and portable LLM sandbox runtime**

LLM Sandbox is a lightweight and portable sandbox environment designed to run large language model (LLM) generated code in a safe and isolated manner using Docker containers. This project aims to provide an easy-to-use interface for setting up, managing, and executing code in a controlled Docker environment, making it ideal for testing and experimenting with LLMs.

### Features

- **Easy Setup:** Quickly create sandbox environments with minimal configuration.
- **Isolation:** Run your code in isolated Docker containers to prevent interference with your host system.
- **Flexibility:** Support for multiple programming languages.
- **Portability:** Use predefined Docker images or custom Dockerfiles.

### Installation

#### Using Poetry

1. Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed.
2. Add the package to your project:

```sh
poetry add llm-sandbox
```

#### Using pip

1. Ensure you have [pip](https://pip.pypa.io/en/stable/installation/) installed.
2. Install the package:

```sh
pip install llm-sandbox
```

### Usage

#### Session Lifecycle

The `SandboxSession` class manages the lifecycle of the sandbox environment, including the creation and destruction of Docker containers. Here’s a typical lifecycle:

1. **Initialization:** Create a `SandboxSession` object with the desired configuration.
2. **Open Session:** Call the `open()` method to build/pull the Docker image and start the Docker container.
3. **Run Code:** Use the `run()` method to execute code inside the sandbox. Currently, it supports Python, Java, JavaScript, C++, Go, and Ruby. See [examples](examples) for more details.
4. **Close Session:** Call the `close()` method to stop and remove the Docker container. If the `keep_template` flag is set to `True`, the Docker image will not be removed, and the last container state will be committed to the image.

### Example

Here's a simple example to demonstrate how to use LLM Sandbox:

```python
from llm_sandbox.session import SandboxSession

# Create a new sandbox session
with SandboxSession(image="python:3.9.19-bullseye", keep_template=True, lang="python") as session:
    # Run some Python code in the sandbox
    result = session.run("print('Hello, World!')")
    print(result)

# With custom Dockerfile
with SandboxSession(dockerfile="Dockerfile", keep_template=True, lang="python") as session:
    # Run some Python code in the sandbox
    result = session.run("print('Hello, World!')")
    print(result)

# Or default image
with SandboxSession(lang="python", keep_template=True) as session:
    # Run some Python code in the sandbox
    result = session.run("print('Hello, World!')")
    print(result)
```


LLM Sandbox also supports copying files between the host and the sandbox:

```python
from llm_sandbox.session import SandboxSession

# Create a new sandbox session
with SandboxSession(lang="python", keep_template=True) as session:
    # Copy a file from the host to the sandbox
    session.copy_to_runtime("test.py", "/sandbox/test.py")

    # Run the copied Python code in the sandbox
    result = session.run("python /sandbox/test.py")
    print(result)

    # Copy a file from the sandbox to the host
    session.copy_from_runtime("/sandbox/output.txt", "output.txt")
```

### API Reference

#### `SandboxSession`

##### Initialization

```python
SandboxSession(
    image: Optional[str] = None,
    dockerfile: Optional[str] = None,
    lang: str = SupportedLanguage.PYTHON,
    keep_template: bool = False,
    verbose: bool = True
)
```

- **image**: Docker image to use.
- **dockerfile**: Path to the Dockerfile, if an image is not provided.
- **lang**: Language of the code (default: `SupportedLanguage.PYTHON`).
- **keep_template**: If `True`, the image and container will not be removed after the session ends.
- **verbose**: If `True`, print messages.

##### Methods

- **`open()`**: Start the Docker container.
- **`close()`**: Stop and remove the Docker container.
- **`run(code: str, libraries: Optional[List] = None)`**: Execute code inside the sandbox.
- **`copy_from_runtime(src: str, dest: str)`**: Copy a file from the sandbox to the host.
- **`copy_to_runtime(src: str, dest: str)`**: Copy a file from the host to the sandbox.
- **`execute_command(command: str)`**: Execute a command inside the sandbox.

### Contributing

We welcome contributions to improve LLM Sandbox! Since I am a Python developer, I am not familiar with other languages. If you are interested in adding better support for other languages, please feel free to submit a pull request.

Here is a list of things you can do to contribute:
- [ ] Add Java maven support.
- [x] Add support for JavaScript.
- [ ] Add support for C++.
- [ ] Add support for Go.
- [ ] Add support for Ruby.
- [ ] Add remote Docker host support.
- [ ] Add remote Kubernetes cluster support.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
