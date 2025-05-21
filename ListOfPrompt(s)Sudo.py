#Author: Puya Pakshad
#This is the List os Prompts we Tested on our Program Source Code dataset through LLM(s) API(s)


# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
#1. Buffer Overflow:

prompt = f"""
You are a cybersecurity expert specialized in detecting buffer overflows in C/C++ programs.

Below are examples of functions, some of which contain buffer overflow vulnerabilities and others that are secure.

[Example 1 - Vulnerable]
void foo(char *input) {{ char buffer[8]; strcpy(buffer, input); }}

ANSWER: 1

[Example 2 - Vulnerable]
void bar() {{ char buffer[5]; gets(buffer); }}

ANSWER: 1

[Example 3 - Secure]
void foo(char *input) {{ char buffer[8]; strncpy(buffer, input, sizeof(buffer) - 1); }}

ANSWER: 0

[Example 4 - Secure]
void bar(char *input) {{ char buffer[8]; snprintf(buffer, sizeof(buffer), "%s", input); }}

ANSWER: 0

Now analyze the following function and determine if it is vulnerable (1) or not (0):

[Function to Analyze]
{function_body}
ANSWER: 
"""
# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #

#2. Use After Free:

prompt = f"""
You are a cybersecurity expert specialized in identifying use-after-free vulnerabilities in C/C++ programs.

See the following examples:

[Example 1 - Vulnerable]
void foo() {{ char *p = malloc(10); free(p); p[0] = 'A'; }}

ANSWER: 1

[Example 2 - Vulnerable]
void bar() {{ int *x = (int*)malloc(sizeof(int)); free(x); printf("%d", *x); }}

ANSWER: 1

[Example 3 - Secure]
void foo() {{ char *p = malloc(10); p[0] = 'A'; free(p); }}

ANSWER: 0

[Example 4 - Secure]
void bar() {{ int *x = malloc(sizeof(int)); if (x) {{ *x = 5; printf("%d", *x); free(x); }} }}

ANSWER: 0

Now analyze the following function and determine if it is vulnerable (1) or not (0):

[Function to Analyze]
{function_body}
ANSWER: 
"""


# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #

#3. Integer Overflow:

prompt = f"""
You are a cybersecurity expert focused on identifying integer overflows in C/C++ code.

Here are a few examples:

[Example 1 - Vulnerable]
int multiply(int a, int b) {{ return a * b; }} // No bounds checking

ANSWER: 1

[Example 2 - Vulnerable]
size_t total = count * sizeof(int); char *p = malloc(total);

ANSWER: 1

[Example 3 - Secure]
int multiply(int a, int b) {{ if (a > INT_MAX / b) return -1; return a * b; }}

ANSWER: 0

[Example 4 - Secure]
if (count <= SIZE_MAX / sizeof(int)) {{ malloc(count * sizeof(int)); }}

ANSWER: 0

Now analyze the following function and determine if it is vulnerable (1) or not (0):

[Function to Analyze]
{function_body}
ANSWER: 
"""

# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #

#4. Format String Vulnerability:

prompt = f"""
You are a cybersecurity expert focused on identifying format string vulnerabilities in C/C++ code.

Below are examples:

[Example 1 - Vulnerable]
void log(char *msg) {{ printf(msg); }}

ANSWER: 1

[Example 2 - Vulnerable]
void error(char *input) {{ fprintf(stderr, input); }}

ANSWER: 1

[Example 3 - Secure]
void log(char *msg) {{ printf("%s", msg); }}

ANSWER: 0

[Example 4 - Secure]
void error(char *input) {{ fprintf(stderr, "%s", input); }}

ANSWER: 0

Now analyze the following function and determine if it is vulnerable (1) or not (0):

[Function to Analyze]
{function_body}
ANSWER: 
"""


# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #

#5. Command Injection:

prompt = f"""
You are a cybersecurity expert analyzing code for command injection vulnerabilities in C/C++.

See the examples below:

[Example 1 - Vulnerable]
void run(char *cmd) {{ char buf[128]; sprintf(buf, "sh -c '%s'", cmd); system(buf); }}

ANSWER: 1

[Example 2 - Vulnerable]
void exec(char *input) {{ execl("/bin/sh", "sh", "-c", input, NULL); }}

ANSWER: 1

[Example 3 - Secure]
void run(char *cmd) {{ if (strcmp(cmd, "ls") == 0) system("ls"); }}

ANSWER: 0

[Example 4 - Secure]
void exec() {{ system("/bin/ls"); }}

ANSWER: 0

Now analyze the following function and determine if it is vulnerable (1) or not (0):

[Function to Analyze]
{function_body}
ANSWER: 
"""


# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #

#6.  Denial of Service (DoS / DDoS) – Resource Exhaustion:

prompt = f"""
You are a cybersecurity expert specialized in identifying Denial of Service (DoS/DDoS) vulnerabilities caused by resource exhaustion in C/C++ applications.

Below are examples of functions. Some are vulnerable to DoS due to unbounded resource usage (e.g., memory, CPU, threads), while others are secure.

[Example 1 - Vulnerable]
void handleRequest(char *input) {{
    while(1) {{}} // Infinite loop, attacker can spawn multiple threads
}}

ANSWER: 1

[Example 2 - Vulnerable]
void process(char *input) {{
    char *buffer = malloc(strlen(input) * 1000000); // Unchecked large allocation
    strcpy(buffer, input);
}}

ANSWER: 1

[Example 3 - Secure]
void handleRequest(char *input) {{
    for(int i = 0; i < 1000; ++i) {{
        // process input with limit
    }}
}}

ANSWER: 0

[Example 4 - Secure]
void process(char *input) {{
    if(strlen(input) > 1024) return;
    char buffer[1024];
    strncpy(buffer, input, sizeof(buffer));
}}

ANSWER: 0

Now analyze the following function and determine if it is vulnerable (1) or not (0):

[Function to Analyze]
{function_body}
ANSWER: 
"""

# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------------- #
