import sys
from invoke import task

RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[94m"
GREEN = "\033[32m"
NO_COLOR = "\033[0m"


def _C(color, message):
    return "{0}{1}{2}".format(color, message, NO_COLOR)


def echo(message, nl=True, color=None):
    if color:
        message = _C(color, message)

    if nl:
        message += "\n"
    sys.stdout.write(message)



def sh(ctx, command, **kwargs):
    kwargs.setdefault('hide', True)
    return ctx.run(command, **kwargs).stdout.strip()


@task
def clean(ctx, docs=False):
    echo("Cleaning the site, build, dist and all __pycache__ directories...", nl=False)
    ctx.run("find gitlint -type d  -name '__pycache__' -exec rm -rf {} \; 2> /dev/null", warn=True)
    ctx.run("rm -rf 'site' 'dist' 'build'")
    echo("DONE", color=GREEN)


@task(pre=[clean])
def stats(ctx):
    echo("*** Code ***")
    ctx.run("radon raw -s gitlint | tail -n 6")
    echo("*** Docs ***")
    echo("    Markdown: {0} lines".format(sh(ctx, "cat docs/*.md | wc -l")))
    echo("*** Tests ***")
    nr_unit_tests = sh(ctx, "py.test gitlint/ --collect-only | grep TestCaseFunction | wc -l")
    nr_int_tests = sh(ctx, "py.test qa/ --collect-only | grep TestCaseFunction | wc -l")
    echo("    Unit Tests: {0}".format(nr_unit_tests))
    echo("    Integration Tests: {0}".format(nr_int_tests))
    echo("*** Git ***")
    echo("    Number of commits: {0}".format(sh(ctx, "git rev-list --all --count", hide=True)))
    echo("    Number of authors: {0}".format(sh(ctx, "git log --format='%aN' | sort -u | wc -l | tr -d ' '")))


@task
def pep8(ctx):
    ignore = "H307,H405,H803,H904,H802,H701"
    exclude = "*settings.py,*.venv/*.py"
    echo("Running flake8...")
    result = sh("flake80 --ignore={0} --max-line-length=120 --exclude={1} gitlint qa examples".format(ignore, exclude))
    pass

    # run_pep8_check(){
    # FLAKE 8
    # H307: like imports should be grouped together
    # H405: multi line docstring summary not separated with an empty line
    # H803: git title must end with a period
    # H904: Wrap long lines in parentheses instead of a backslash
    # H802: git commit title should be under 50 chars
    # H701: empty localization string
    # FLAKE8_IGNORE = "H307,H405,H803,H904,H802,H701"
    # exclude settings files and virtualenvs
    # FLAKE8_EXCLUDE = "*settings.py,*.venv/*.py"
    # echo - ne
    # "Running flake8..."
    # RESULT =$(flake8 - -ignore =$FLAKE8_IGNORE - -max - line - length = 120 - -exclude =$FLAKE8_EXCLUDE
    # gitlint
    # qa
    # examples)
    # local
    # exit_code =$?
    # handle_test_result
    # "$RESULT"
    # return $exit_code
