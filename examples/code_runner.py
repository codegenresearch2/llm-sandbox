from llm_sandbox import SandboxSession

def run_code(session, code: str, libraries: list = None):
    if libraries:
        session.execute_command(f"pip install {' '.join(libraries)}")

    output = session.run(code)
    print(output)

def run_python_code():
    with SandboxSession(lang="python", keep_template=True, verbose=True) as session:
        output = run_code(session, "print('Hello, World!')")

        output = run_code(session, """
import numpy as np
print(np.random.rand())
""", libraries=["numpy"])

        session.execute_command("pip install pandas")
        output = run_code(session, """
import pandas as pd
print(pd.__version__)
""")

        session.copy_to_runtime("README.md", "/sandbox/data.csv")

def run_java_code():
    with SandboxSession(lang="java", keep_template=True, verbose=True) as session:
        output = run_code(session, """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
""")

def run_javascript_code():
    with SandboxSession(lang="javascript", keep_template=True, verbose=True) as session:
        output = run_code(session, "console.log('Hello, World!')")

        output = run_code(session, """
const axios = require('axios');
axios.get('https://jsonplaceholder.typicode.com/posts/1')
    .then(response => console.log(response.data));
""", libraries=["axios"])

def run_cpp_code():
    with SandboxSession(lang="cpp", keep_template=True, verbose=True) as session:
        output = run_code(session, """
#include <iostream>
int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
""")

        output = run_code(session, """
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

        output = run_code(session, """
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

if __name__ == "__main__":
    run_python_code()
    run_java_code()
    run_javascript_code()
    run_cpp_code()