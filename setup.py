from cx_Freeze import setup, Executable
# import os

base = None
# desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
executables = [Executable(
    script="main.py", base=base, icon="league.ico", target_name="TikTok_Scraper"
)]

packages = ["selenium", "prettytable", "pprint", 'pyfiglet']
options = {
    'build_exe': {
        'packages': packages,
        'include_files': ['chromedriver.exe']

    },
}

setup(
    name="Titok Scraper",
    options=options,
    version="1.0",
    description="It's bot that parse information about specific name in account",
    executables=executables
)
