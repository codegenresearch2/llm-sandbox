import os
import docker
import docker.errors
from typing import List, Optional

from docker import DockerClient
from llm_sandbox.const import SupportedLanguage, DefaultImage, NotSupportedLibraryInstallation, SupportedLanguageValues

def image_exists(client: DockerClient, image: str) -> bool:
    """
    Check if a Docker image exists.

    Parameters:
    client (DockerClient): Docker client.
    image (str): Docker image.

    Returns:
    bool: True if the image exists, False otherwise.
    """
    try:
        client.images.get(image)
        return True
    except docker.errors.ImageNotFound:
        return False
    except Exception as e:
        raise e

def get_libraries_installation_command(lang: str, libraries: List[str]) -> Optional[str]:
    """
    Get the command to install libraries for the given language.

    Parameters:
    lang (str): Programming language.
    libraries (List[str]): List of libraries.

    Returns:
    Optional[str]: Installation command as a single string.
    """
    if lang in NotSupportedLibraryInstallation:
        return None

    if lang == SupportedLanguage.PYTHON:
        return f"pip install {' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVA:
        return f"mvn install:install-file -Dfile={' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return f"yarn add {' '.join(libraries)}"
    elif lang == SupportedLanguage.CPP:
        return f"apt-get update && apt-get install -y {' '.join(libraries)}"
    elif lang == SupportedLanguage.GO:
        return f"go get {' '.join(libraries)}"
    elif lang == SupportedLanguage.RUBY:
        return f"gem install {' '.join(libraries)}"
    else:
        raise ValueError(f"Language {lang} is not supported")

def get_code_file_extension(lang: str) -> str:
    """
    Get the file extension for the given language.

    Parameters:
    lang (str): Programming language.

    Returns:
    str: File extension.
    """
    if lang == SupportedLanguage.PYTHON:
        return "py"
    elif lang == SupportedLanguage.JAVA:
        return "java"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return "js"
    elif lang == SupportedLanguage.CPP:
        return "cpp"
    elif lang == SupportedLanguage.GO:
        return "go"
    elif lang == SupportedLanguage.RUBY:
        return "rb"
    else:
        raise ValueError(f"Language {lang} is not supported")

def get_code_execution_command(lang: str, code_file: str) -> List[str]:
    """
    Get the command to execute the code.

    Parameters:
    lang (str): Programming language.
    code_file (str): Path to the code file.

    Returns:
    List[str]: Execution command as a list of strings.
    """
    if lang == SupportedLanguage.PYTHON:
        return [f"python {code_file}"]
    elif lang == SupportedLanguage.JAVA:
        return [f"javac {code_file}", f"java {os.path.splitext(code_file)[0]}"]
    elif lang == SupportedLanguage.JAVASCRIPT:
        return [f"node {code_file}"]
    elif lang == SupportedLanguage.CPP:
        return [f"g++ -o a.out {code_file}", "./a.out"]
    elif lang == SupportedLanguage.GO:
        return [f"go run {code_file}"]
    elif lang == SupportedLanguage.RUBY:
        return [f"ruby {code_file}"]
    else:
        raise ValueError(f"Language {lang} is not supported")

def run_code(lang: str, code: str, libraries: List[str] = None):
    """
    Run the given code in a Docker container.

    Parameters:
    lang (str): Programming language.
    code (str): Code to run.
    libraries (List[str], optional): List of libraries to install. Defaults to None.
    """
    client = docker.from_env()
    image = getattr(DefaultImage, lang.upper())

    if not image_exists(client, image):
        client.images.pull(image)

    container = client.containers.create(image, tty=True)

    code_file = f"code.{get_code_file_extension(lang)}"
    container.put_archive('/sandbox', code.encode())

    commands = []
    if libraries:
        install_command = get_libraries_installation_command(lang, libraries)
        if install_command:
            commands.append(install_command)

    commands.extend(get_code_execution_command(lang, f"/sandbox/{code_file}"))

    for command in commands:
        exit_code, output = container.exec_run(command, stream=True)
        if exit_code != 0:
            raise Exception(f"Command '{command}' failed with exit code {exit_code}")
        print(output.decode())

    container.remove()

if __name__ == "__main__":
    for lang in SupportedLanguageValues:
        if lang == SupportedLanguage.PYTHON:
            run_code(lang, "print('Hello, World!')", libraries=["numpy"])
            run_code(lang, "import numpy as np\nprint(np.random.rand())")
            run_code(lang, "import pandas as pd\nprint(pd.__version__)", libraries=["pandas"])
        elif lang == SupportedLanguage.JAVA:
            run_code(lang, """
            public class Main {
                public static void main(String[] args) {
                    System.out.println("Hello, World!");
                }
            }
            """)
        elif lang == SupportedLanguage.JAVASCRIPT:
            run_code(lang, "console.log('Hello, World!')")
            run_code(lang, """
            const axios = require('axios');
            axios.get('https://jsonplaceholder.typicode.com/posts/1')
                .then(response => console.log(response.data));
            """, libraries=["axios"])
        elif lang == SupportedLanguage.CPP:
            run_code(lang, """
            #include <iostream>
            int main() {
                std::cout << "Hello, World!" << std::endl;
                return 0;
            }
            """)
            run_code(lang, """
            #include <iostream>
            #include <vector>
            int main() {
                std::vector<int> v = {1, 2, 3, 4, 5};
                for (int i : v) {
                    std::cout << i << " ";
                }
                std::cout << std::endl;
                return 0;
            }
            """)
            run_code(lang, """
            #include <iostream>
            #include <vector>
            #include <algorithm>
            int main() {
                std::vector<int> v = {1, 2, 3, 4, 5};
                std::reverse(v.begin(), v.end());
                for (int i : v) {
                    std::cout << i << " ";
                }
                std::cout << std::endl;
                return 0;
            }
            """, libraries=["libstdc++"])