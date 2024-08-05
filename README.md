# zabbix-template-to-markdown
A simple python script that takes a zabbix yaml template and converts it to markdown. Very helpful when trying to create README files for git repos. Feel free to use.

## Requirements
- Python 3.6+
- PyYAML library

## How to use
- Install dependencies using pip
`pip install -r requirements.txt` or `pip install pyyaml`
- Run the script inputting the absolute or relative path of the template yaml to the script:
<p>Example:</p>
```bash
python template_to_md.py ./template_file.yaml 
```

## License
Licensed under MIT license.
