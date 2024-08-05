import yaml
import sys
import re

def main(source_file):

	pattern = re.compile(r'(?:.*[\/\\])?(.*)')
	match = pattern.match(source_file)
	if match:
		final_file = match.group(1).split('.yaml')[0] + '.md'
	else:
		print('Could not extract the final file name. Using default: zabbix_template.md')
		final_file = 'zabbix_template.md'

	with open(source_file, 'r') as file:
		yaml_content = yaml.safe_load(file)

	templates = yaml_content['zabbix_export']['templates']

	for template in templates:
		template_name = template['name']
		template_descr = template['description']

		items = []
		triggers = []

		for item in template['items']:
			new_item = {}
			new_item['name'] = item['name']
			new_item['type'] = item['type']
			new_item['key'] = item['key'].replace('\n', ' ')

			if 'description' in item:
				new_item['description'] = item['description'].replace('\n', ' ')
			else:
				new_item['description'] = '<p>LLD</p>'

			items.append(new_item)

			if 'triggers' in item:
				for trigger in item['triggers']:
					new_trigger = {}
					new_trigger['name'] = trigger['name']
					new_trigger['expression'] = '<p>**Expression**: ' + trigger['expression'].replace('\n', ' ') + '</p>'
					new_trigger['priority'] = trigger['priority']
					if 'description' in trigger:
						new_trigger['description'] = trigger['description'].replace('\n', ' ')
					else:
						new_trigger['description'] = '<p>-</p>'

					if 'recovery_expression' in trigger:
						new_trigger['recovery_expression'] = ('<p>**Recovery expression**: ' + trigger['recovery_expression'].replace('\n', ' ') + '</p>')

					triggers.append(new_trigger)


		discoveries = []

		for discovery in template['discovery_rules']:
			new_discovery = {}
			new_discovery['name'] = discovery['name']
			new_discovery['key'] = discovery['key']
			new_discovery['type'] = discovery['type']
			new_discovery['description'] = discovery['description'].replace('\n', ' ')

			discoveries.append(new_discovery)

			if 'item_prototypes' in discovery:
				for item in discovery['item_prototypes']:
					new_item = {}
					new_item['name'] = item['name']
					new_item['type'] = item['type']
					new_item['key'] = item['key'].replace('\n', ' ') + '<p>LLD</p>'
					new_item['description'] = item['description'].replace('\n', ' ')

					items.append(new_item)

			if 'trigger_prototypes' in discovery:
				for trigger in discovery['trigger_prototypes']:
					new_trigger = {}
					new_trigger['name'] = trigger['name']
					new_trigger['expression'] = '<p>**Expression**: ' + trigger['expression'].replace('\n', ' ') + '</p>'
					new_trigger['priority'] = trigger['priority']
					new_trigger['description'] = trigger['description'].replace('\n', ' ')

					if 'recovery_expression' in trigger:
						new_trigger['expression'] += ('<p>**Recovery expression**: ' + trigger['recovery_expression'].replace('\n', ' ') + '</p>')

					triggers.append(new_trigger)

		macros = []

		for macro in template['macros']:
			new_macro = {}
			new_macro['name'] = macro['macro']
			new_macro['value'] = macro['value'].replace('|',r'\|')
			if 'description' in macro:
				new_macro['description'] = macro['description'].replace('\n', ' ')
			else:
				new_macro['description'] = '<p>-</p>'

			macros.append(new_macro) 


	final_md_file = ''

	final_md_file += f"{template_name}\n"
	final_md_file += "## Overview\n\n"
	final_md_file += "--> Put overview here <--\n\n"
	final_md_file += "## Author\n\n"
	final_md_file += "--> Put author here <--\n\n"
	final_md_file += "## Macros used\n\n"
	final_md_file += "|Name|Description|Default|Type|\n"
	final_md_file += "|----|-----------|----|----|\n"
	for macro in macros:
		final_md_file += f"|{macro['name']}|{macro['description']}|`{macro['value']}`|Text macro|\n"
	final_md_file += "\n"
	final_md_file += "## Template links\n\nThere are no template links in this template\n\n"
	final_md_file += "## Discovery rules\n\n"
	final_md_file += "|Name|Description|Type|Key and additional info|\n"
	final_md_file += "|----|-----------|----|----|\n"
	for disco in discoveries:
		final_md_file += f"|{disco['name']}|{disco['description']}|{disco['type']}|{disco['key']}|\n"
	final_md_file += "\n"
	final_md_file += "## Items collected\n\n"
	final_md_file += "|Name|Description|Type|Key and additonal info|\n"
	final_md_file += "|----|-----------|----|----|\n"
	for item in items:
		final_md_file += f"|{item['name']}|{item['description']}|`{item['type']}`|{item['key']}|\n"
	final_md_file += "\n"
	final_md_file += "## Triggers\n\n"
	final_md_file += "|Name|Description|Expression|Priority|\n"
	final_md_file += "|----|-----------|----|----|\n"
	for trig in triggers:
		final_md_file += f"|{trig['name']}|{trig['description']}|{trig['expression']}|{trig['priority']}|\n"

	with open(final_file, 'w') as f:
		f.write(final_md_file)

if __name__ == "__main__":

	if len(sys.argv) == 1:
		print('No arguments passed. Please pass the absolute path of the input .yaml as an argument to start the procedure...')
	if len(sys.argv) > 2:
		print('More than 1 arguments passed. Please pass only the absolute path of the input .yaml as an argument to start the procedure...')
	
	source_file = sys.argv[1]
	
	main(source_file)
