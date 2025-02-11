from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_libraries_installation_command, get_code_execution_command

def run_code(lang: str, code: str, libraries: list = None):
    with SandboxSession(lang=lang, keep_template=True, verbose=True) as session:
        if libraries:
            install_command = get_libraries_installation_command(lang, libraries)
            session.execute_command(install_command)

        output = session.run(code)
        print(output)

def execute_python_code():
    run_code('python', "print('Hello, World!')")
    run_code('python', "import numpy as np\nprint(np.random.rand())", libraries=['numpy'])
    run_code('python', "import pandas as pd\nprint(pd.__version__)", libraries=['pandas'])
    session.copy_to_runtime('README.md', '/sandbox/data.csv')

def execute_java_code():
    run_code('java', """
        public class Main {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
    """)

def execute_javascript_code():
    run_code('javascript', "console.log('Hello, World!')")
    run_code('javascript', """
        const axios = require('axios');
        axios.get('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => console.log(response.data));
    """, libraries=['axios'])

def execute_cpp_code():
    run_code('cpp', """
        #include <iostream>
        int main() {
            std::cout << "Hello, World!" << std::endl;
            return 0;
        }
    """)
    run_code('cpp', """
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
    run_code('cpp', """
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
    """, libraries=['libstdc++'])

if __name__ == '__main__':
    execute_python_code()
    execute_java_code()
    execute_javascript_code()
    execute_cpp_code()