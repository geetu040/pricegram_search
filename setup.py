import os
import json
import gdown
import tensorflow as tf
import tensorflow_hub as hub

# 0. Loading the download configuration
with open('config.json', 'rb') as f:
	CONFIG = json.load(f)

# 1. Creating Dump Folder
root = CONFIG['dump_folder_path']
if not os.path.exists(root):
	os.makedirs(root)

# 2. Loading versions of previous downloads
version_file_path = os.path.join(root, CONFIG['version_file_name'])
if os.path.exists(version_file_path):
	with open(version_file_path, 'rb') as f:
		versions = json.load(f)
else:
	versions = {}

# 3. Downloading Utils

print_bar_len = 20
for dump in CONFIG['dumps']:
	name, type, path, v, info = list(dump.values())
	path = os.path.join(root, path)

	if versions.get(path) == v:
		print(f" Already Up to Date {name} [v:{v}] ".join(["=" * print_bar_len] * 2))
		continue

	print(f" Downloading {name} [v:{v}] ".join(["=" * print_bar_len] * 2))

	if type == "gdown":
		gdown.download(
			f"https://drive.google.com/uc?id={info['id']}",
			path,
			quiet=False
		)
	elif type == "tf_hub":
		embed = hub.load(info['url'])
		tf.saved_model.save(embed, path)

	versions[path] = v

# 4. Saving Latest Versions

with open(version_file_path, 'w') as f:
	json.dump(versions, f)

