# Melanippe
Python CLI tool for profiling databases

Started as a one-off script in my ML repo.
Going to try making it into something more useful.

Goal:

Quickly get a lot of useful information about your database. Things like:

Size on disk
Table metadata
Schema
Configuration

Useful info is exported to csv.

You can then do a cron and regularly take diffs to see how things change.
You can also export to Google Docs.

TODO:
  - Add configuration / setup
  - Add intelligence to support different environments and OS's.
  - Add functionality to export to Google docs
  - Add postgresql support
  - Add mongodb support
  - Add sqlite support
  - Add tests
