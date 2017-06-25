# Real-Time-LaTeX
Easily set up a vanilla TeX Live environment and run a python script to compile LaTeX source code in real-time. Supports Ubuntu and Windows 10 with the Windows Subsystem for Linux (WSL).

## Installation

### Windows 10 Only

1) Install the Windows Subsystem for Linux: https://msdn.microsoft.com/en-us/commandline/wsl/install_guide
2) Open a command prompt window and run `bash`.

### Windows 10 and Ubuntu

1) Download the code from GitHub: Within Bash, run `cd ~ && git clone https://github.com/stevenengler/Real-Time-LaTeX.git`. You can clone it somewhere else of course, but the home directory makes it easy to access later.
2) Run the installation script: Within Bash, run `cd Real-Time-LaTeX && ./installer.sh`.
3) Follow the instructions to install TeX Live, python3-watchdog, and latexmk.

## How to Use

### Setting the configuration file

The compiler script works with LaTeX "projects". A project is just a directory containing all of your LaTeX source code, as well as a `latex_project.config` file. The `latex_project.config` file should contain a single line with the path to the tex file which should be compiled. For example, if you have the LaTeX document directory structure like the following:

```
my_report
├── src
│   ├── chapter1.tex
│   ├── chapter2.tex
│   └── report.tex
├── compiled
│   ├── report.pdf
│   └── report.log
```

Just create a `my_report/latex_project.config` file containing the line `src/report.tex`.

### Running the compiler script

Open a command prompt window with Bash in your project directory (the `my_report` directory in the example above). Run the command `python3 ~/Real-Time-LaTeX/compile.py`. Now anytime you make a change to a \*.tex file in your project folder, the tex file linked to from your `latex_project.config` file will be compiled into the `compiled` directory.
