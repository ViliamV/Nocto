# nocto

Simple CLI tool to replace [Octopus](https://octopus.com/)-style templated variables in file from local environment.

Simple example:

```bash
kubectl apply -f $(nocto replace deployment.yaml)
```

## Installation

```bash
pipx install nocto

# OR

pip install --user nocto
```

## Usage

```bash
 Usage: nocto [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                     │
│ --show-completion             Show completion for the current shell, to copy it or          │
│                               customize the installation.                                   │
│ --help                        Show this message and exit.                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────╮
│ replace  Replaces all Octopus-style template variables in `file` and writes it to temporary │
│          file. Returns path to temporary file.                                              │
│ test     Tests if local environment has all the variables required to replace Octopus-stype │
│          templated variables in `file`.                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Test command

```bash
 Usage: nocto test [OPTIONS] FILE

 Tests if local environment has all the variables required to replace Octopus-stype templated
 variables in `file`.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────╮
│ *    file      FILE  File in which to replace variables [default: None] [required]          │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮
│ --dotenv         --no-dotenv          Use dotenv to load .env file [default: no-dotenv]     │
│ --dotenv-file                   FILE  Optional .env file to use [default: None]             │
│ --var                           TEXT  Directly set variable value. E.g. FOO=BAR             │
│                                       [default: None]                                       │
│ --help                                Show this message and exit.                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Replace command

```bash
 Usage: nocto replace [OPTIONS] FILE

 Replaces all Octopus-style template variables in `file` and writes it to temporary file.
 Returns path to temporary file.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────╮
│ *    file      FILE  File in which to replace variables [default: None] [required]          │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮
│ --dotenv         --no-dotenv          Use dotenv to load .env file [default: no-dotenv]     │
│ --dotenv-file                   FILE  Optional .env file to use [default: None]             │
│ --var                           TEXT  Directly set variable value. E.g. FOO=BAR             │
│                                       [default: None]                                       │
│ --help                                Show this message and exit.                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```
