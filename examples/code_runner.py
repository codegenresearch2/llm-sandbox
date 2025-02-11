from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_libraries_installation_command, get_code_file_extension
from llm_sandbox.const import SupportedLanguage

def run_python_code():
    with SandboxSession(lang=SupportedLanguage.PYTHON, keep_template=True, verbose=True) as session:
        output = session.run("print('Hello, World!')")
        print(output)

        session.execute_command(get_libraries_installation_command(SupportedLanguage.PYTHON, ["numpy"]))
        output = session.run("import numpy as np\nprint(np.random.rand())")
        print(output)

        session.execute_command(get_libraries_installation_command(SupportedLanguage.PYTHON, ["pandas"]))
        output = session.run("import pandas as pd\nprint(pd.__version__)")
        print(output)

def run_java_code():
    with SandboxSession(lang=SupportedLanguage.JAVA, keep_template=True, verbose=True) as session:
        output = session.run("""
        public class Main {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """)
        print(output)

def run_javascript_code():
    with SandboxSession(lang=SupportedLanguage.JAVASCRIPT, keep_template=True, verbose=True) as session:
        output = session.run("console.log('Hello, World!')")
        print(output)

        session.execute_command(get_libraries_installation_command(SupportedLanguage.JAVASCRIPT, ["axios"]))
        output = session.run("""
        const axios = require('axios');
        axios.get('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => console.log(response.data));
        """)
        print(output)

def run_cpp_code():
    with SandboxSession(lang=SupportedLanguage.CPP, keep_template=True, verbose=True) as session:
        output = session.run("""
        #include <iostream>
        int main() {
            std::cout << "Hello, World!" << std::endl;
            return 0;
        }
        """)
        print(output)

        output = session.run("""
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
        print(output)

        session.execute_command(get_libraries_installation_command(SupportedLanguage.CPP, ["libstdc++"]))
        output = session.run("""
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
        """)
        print(output)

if __name__ == "__main__":
    run_cpp_code()