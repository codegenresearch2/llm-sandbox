import os
from typing import List
from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_libraries_installation_command, get_code_execution_command, get_code_file_extension
from llm_sandbox.const import SupportedLanguage

def run_code(lang: str, code: str, libraries: List[str] = None):
    output_dir = f'output_{lang}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with SandboxSession(lang=lang, keep_template=True, verbose=True) as session:
        if libraries:
            install_command = get_libraries_installation_command(lang, libraries)
            session.execute_command(install_command)

        code_file = f'code.{get_code_file_extension(lang)}'
        with open(os.path.join(output_dir, code_file), 'w') as f:
            f.write(code)

        session.copy_to_runtime(code_file, f'/sandbox/{code_file}')
        execution_commands = get_code_execution_command(lang, code_file)
        for command in execution_commands:
            output = session.run(command)
            print(output)

if __name__ == '__main__':
    python_code = """
    print('Hello, World!')
    import numpy as np
    print(np.random.rand())
    import pandas as pd
    print(pd.__version__)
    """
    run_code(SupportedLanguage.PYTHON, python_code, libraries=['numpy', 'pandas'])

    java_code = """
    public class Main {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }
    }
    """
    run_code(SupportedLanguage.JAVA, java_code)

    javascript_code = """
    console.log('Hello, World!')
    const axios = require('axios');
    axios.get('https://jsonplaceholder.typicode.com/posts/1')
        .then(response => console.log(response.data));
    """
    run_code(SupportedLanguage.JAVASCRIPT, javascript_code, libraries=['axios'])

    cpp_code = """
    #include <iostream>
    int main() {
        std::cout << "Hello, World!" << std::endl;
        return 0;
    }
    """
    run_code(SupportedLanguage.CPP, cpp_code)

    cpp_code_with_lib = """
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
    """
    run_code(SupportedLanguage.CPP, cpp_code_with_lib, libraries=['libstdc++'])