Contributing
============

Thanks for signing the guestbook!  You do not need previous open-source
experience.

Add your entry
--------------

1. Fork this repository on GitHub.
2. Clone the fork to your computer.
3. Create `./contributors/<your-github-username>.txt` - the filename *must* be
   all lowercase.
4. Add one line like this:

   ```
   Your-GitHub-Username was here 😎
   ```

   Capitalization is completely flexible inside this file.  The emoji, believe
   it or not, is required - although you can use whichever emoji you'd like.
5. Make sure the file ends with a newline - most text editors do this
   automatically.
6. Check it locally:

   ```
   $ ./tools/validate-file ./contributors/your-github-username.txt
   OK: ./contributors/your-github-username.txt
   ```

7. Commit and push your change, then open a pull request.

Updating or removing your entry
--------------------------------

You may later edit or delete your own file in a new pull request - the PR author
must match the file being modified.

Format
------

```
<username> was here <emoji>\n
```

Where `<username>` is a valid GitHub username and `<emoji>` is a single emoji
(or visible Unicode code point).

### Rules

- You must use your own GitHub username (the same name that authors the pull
  request).
- The filename must use your lowercase GitHub login and end in `.txt`.
- The username inside the file may use any capitalization, but it must otherwise
  match the filename.
- Use exactly one space between words: ex: `dave< >was< >here< >😎`.
- The file must contain exactly one line and end with a newline.
- The final item must be one emoji or single Unicode code point.
- The file must not exceed 1024 bytes.

Notes
-----

The `validate-file` checker requires Perl 5 as it can correctly parse and
understand Unicode grapheme / compound emoji as one visible character.  If your
system does not have that that's fine - the CI that GitHub will perform has perl
and can validate the file.

---

The rules and format of the text file might seem surprisingly strict - that is
by design.  I want to make it easy for people new to git and GitHub to get their
feet wet with a project that is incredibly low-stakes, but has a somewhat
involved validation process.  This way, they'll feel comfortable in the future
when it comes to make a pull-request to a "real" project.

So remember, this project is low-stakes!  Don't be afraid to create a PR and see
that it breaks the validator - that's the point of the validator! Pushing a
change that is invalid is part of the learning process - don't feel worried or
scared of that.
