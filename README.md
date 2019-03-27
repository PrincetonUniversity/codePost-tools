# codePost Princeton Tools

The tools in this repository were written to provide convenient access to the [codePost](https://codepost.io) platform from Princeton University's Department of Computer Science. They make a set of assumptions to simplify to workflow of uploading assignments to codePost from submissions made by students to [TigerFile](https://csguide.cs.princeton.edu/academic/tigerfile), the submission platform provided by the department's IT staff (including [@jcrouth](https://github.com/jcrouth)).

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

   ```yaml
   api_key: "<API KEY HERE>" # <-- obtain your codePost API key from https://codepost.io/settings

   # Course specific settings
   course_name: COS126
   course_period: S2019

   # TigerFile specific settings (do not change)
   tigerfile_path: /n/fs/tigerfile/Files/{course_name}_{course_period}/{assignment_name}
   user_pattern: "{}@princeton.edu"
   partners_path: "{pwd}/partners.txt"
   group_separator: "-"

   # Run-script specific settings (for COS 126, 226, ..., comment out if not using)
   tests_path: "{pwd}/../.output/{submission}.output.txt"

   # LMS column IDs (optional, for convenient grade export, comment out if not using)
   lms_format: "{name} | {id}"
   lms_ids:
     Hello: 38213
     Loops: 38235
   ```

## Command Line Syntax

### Upload tool

```
$ push-to-codePost --help
usage: push-to-codePost [-h] [-a A] [-s S [S ...]] [--netid] [--groupname]
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

### Grade export tool

```
$ export-codePost-grades --help
usage: export-codePost-grades [-h] [-a [A [A ...]]] [-n [N [N ...]]]
                              [--blackboard] [--pretty] [--json]
                              [--include-inactive] [--include-empty]
                              [--verbose]

optional arguments:
  -h, --help          show this help message and exit
  -a [A [A ...]]      Name(s) of the assignment(s) for which to export grades
                      (by default, all available).
  -n [N [N ...]]      Usernames of students to export (by default, everybody).
  --blackboard        Insert Blackboard column IDs when available (in
                      configuration file, the "lms_ids" option).
  --pretty            Pretty print output.
  --json              Export as JSON (by default, the export is CSV).
  --include-inactive  Include the grades of students who are inactive.
  --include-empty     Include columns for assignments even when the column is
                      blank.
  --verbose           Display informational messages.
```

## Usage Examples

In both the following examples, we asssume there is a configuration file `~/.codepost-config.yaml` which is properly configured for the course `"COS126"` and period `"S2019"`. We assume that the autograding scripts can be invoked by calling `~/assignments/guitar/run-script *`.

### Upload a single submission

When uploading a single submission, it is more convenient to copy from the `by_netid` folder and to use the `--netid` upload mode.

```shell
$ cd $(mktemp -d)
$ cp -pr /n/fs/tigerfile/Files/COS126_S2019/Guitar/by_netid/jstudent ./
$ ~/assignment/guitar/run-script *
$ push-to-codePost --netid -a 'Guitar' -s jstudent
```

### Upload many submissions

When uploading a batch of submissions, it is better to copy submissions from the `submissions` folder.

```shell
$ cd $(mktemp -d)
$ cp -pr /n/fs/tigerfile/Files/COS126_S2019/Guitar/submissions/* ./
$ ~/assignment/guitar/run-script *
$ push-to-codePost -a 'Guitar' -s *
```

### Export grades to CSV to import in Blackboard

It is possible to export all grades associated with the current course (as defined by the configuration file) using the `export-codePost-grades` tool. If the configuration has been properly configured, such that the `lms_ids` section contains the column identifiers of the Blackboard Gradecenter, then it is possible to produce a CSV that can be directly imported by Blackboard using the `--blackboard` flag:

```shell
$ export-codePost-grades -a Hello Loops --blackboard > course_grades.csv
$ head -3 course_grades.csv
"Username","Hello | 38213","Loops | 38235"
"student1",20.0,20.0
"student2",20.0,20.0
```

For the Blackboard export to work, you need to complete the section `lms_ids` of the configuration file:

```yaml
lms_ids:
  Hello: 38213
  Loops: 38235
```

where, for each assignment name, you provide the column identifier of the corresponding column in Blackboard. You can obtain a column's identifier in Blackboard's Gradecenter by using the [grade column menus](https://help.blackboard.com/Learn/Instructor/Grade/Grade_Columns#menu-options_OTP-3).

To give you an example of the content of the `course_grades.csv` file, consider the following output:

```shell
$ export-codePost-grades --pretty | head -3
"Username","Loops","Sierpinski","Programming Exam 1","NBody","Hello"
"student1",   20.0,            ,                11.0,   20.0,   20.0
"student2",   20.0,        20.0,                15.0,   20.0,   20.0
```

## Remarks

### About partnerships...

- If you are not using TigerFile, or running this tool outside of the Princeton CS infrastructure, you will lose partnerships detection. One way to circumvent this, is to use the `--groupname` mode, and to include all the student usernames of a partnerships in the directory name, separated by dashes, such as `partner1-partner2`.

- Another mechanism to specify partnerships, which also does not depend on TigerFile, is to include the student usernames, one by line, in a file `partners.txt` included in each submission folder, in addition to the other files. When this file is detected, the upload tool will use this information. (You can change the name of the file containing this information by adjusting the `partners_path` setting in the configuration file.)

### About TigerFile...

- The root tree of TigerFile submissions is located on the CS department's NFS at: `/n/fs/tigerfile/Files/`.

- When creating a course, use the same naming conventions used throughout Princeton, both for the course name `"COSxxx"` and the course period `"S2019"`, for Spring 2019, (in both cases with no spaces). This is important to properly resolve the path associated with your course in TigerFile's tree.

- If you have an assignment that contains a space in its name, such as `"My Assignment"`, the associated TigerFile will substitute the space `" "` by an underscore `"_"`; you must be sure to use quotes when specifying the assignment name in the command line call.

- The directory tree for the submissions to `"My Assignment"` in course `"COS101"` taught during `"S2019"` would be `/n/fs/tigerfile/Files/COS101_S2019/My_Assignment/`. There are two subdirectories: `submissions` contains a folder per submission; `by_netid` contains a folder per student (and so some submissions are duplicated as they appear for each student).

- You can find more general information about [Tigerfile on the CS guide](https://csguide.cs.princeton.edu/academic/tigerfile).

### About RunScript...

- The autograders used in Princeton CS' intro courses typically outputs the result of processing a submission in the hidden folder `.output`, such that the result of submission `XXXXXX` would be available as `.output/XXXXXX.output.txt`. This can be changed in this part of the configuration file (or commented out if not using these autograders):

  ```yaml
  # Run-script specific settings (for COS 126, 226, etc., comment out if not using)
  tests_path: "{pwd}/../.output/{submission}.output.txt"
  ```

- You can find more general information about [RunScript on the CS guide](https://csguide.cs.princeton.edu/academic/runscript).
