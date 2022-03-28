import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='EasyRedditScraper',
    version='0.0.1',
    author='https://github.com/rick433/',
    url="https://github.com/rick433/EasyRedditScraper",
    description='Easy to use downloader for reddit media.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['EasyRedditScraper'],
    license='MIT',
    install_requires=['tqdm'],
)
