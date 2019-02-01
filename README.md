# Links Finder
A webcrawler to list all the links within a page or a group of pages

## Requirements
- Python3.6 or higher

## Getting started
To install all the dependencies, execute the following command within the project folder.

```
pip install -r requirements
```
## How to use
There are two parameters:

    --url (obligatory): receives an url
    --recursive (optional, False by default): if True search for links in the subpages of the given pages (this may take a while), otherwise search for links in the given page only.

After the execution, a .txt file will be created in the project folder containing all the links found.

## E.G.:

```
    python webCrawler --url https://github.com/EduardoMCF/Links-Finder
```

```
    python webCrawler --url https://github.com/EduardoMCF/Links-Finder --recursive True
```

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**