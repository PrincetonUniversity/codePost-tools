# codePost Princeton Tools

The tools in this repository were written to provide convenient access to the codePost platform from Princeton University's Department of Computer Science. They make a set of assumptions to simplify to workflow of upload assignments to codePost from submissions made by students to [Tigerfile](https://csguide.cs.princeton.edu/academic/tigerfile), the submission provided by the department's IT staff (including @jcrouth).

## Quick Setup

1. Install the codePost Princeton Tools to your path using pip:

```
pip install --upgrade codePost-princeton-tools
```

If you do not have sufficient privileges to install the tools globally, you can install them in your home directory:

```
pip install --user --upgrade codePost-princeton-tools
```

2. Retrieve your codePost API key from codePost's settings at [https://codepost.io/settings](https://codepost.io/settings). Note that as of March 2019, you can only retrieve a codePost API key if you are an administrator for a course on codePost.

3. Create a configuration file in your home directory, either called `codepost-config.yaml` or `.codepost-config.yaml`, and complete the following template for the information relevant to your course. You should at most have to add the codePost API key, and set the proper course name and period.

```
api_key: "<API KEY HERE>" # <-- obtain your codePost API key from https://codepost.io/settings

# Course specific settings
course_name: COS126
course_period: S2019

# Tigerfile specific settings (do not change)
tigerfile_path: /n/fs/tigerfile/Files/{course_name}_{course_period}/{assignment_name}
user_pattern: "{}@princeton.edu"
partners_path: "{pwd}/partners.txt"
group_separator: "-"

# Run-script specific settings (for COS 126, 226, etc., comment out if not using)
tests_path: "{pwd}/../.output/{submission}.output.txt"
```

## Command Line Syntax

```
$ push-to-codePost2 --help
usage: push-to-codePost2 [-h] [-a A] [-s S [S ...]] [--netid] [--groupname]
                         [--extend] [--overwrite] [--verbose]
                         [--without-tests] [--use-cache] [--skip-notdone]

optional arguments:
  -h, --help       show this help message and exit
  -a A             The name of the assignment to upload to (e.g. Loops)
  -s S [S ...]     The list of folders, one folder per submission to upload.
  --netid          Assume each folder name is a different NetID instead of
                   submission hashes, and resolve partners. [NOT RECOMMENDED]
  --groupname      Assume each folder name contains all NetIDs of a group, of
                   submission hashes.
  --extend         If submission already exists, add new files to it and
                   replace old files if the code has changed.
  --overwrite      If submission already exists, overwrite it.
  --verbose        Display informational messages.
  --without-tests  Allow upload assignments that do not have compiled tests.
  --use-cache      Allow for caching mechanism (i.e., for groups).
  --skip-notdone   Skip submissions that are not done.
```

## Usage Examples

### Upload a single submission

### Upload many submissions
