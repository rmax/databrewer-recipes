"""A script to validate datasets definitions."""
import argparse
import glob
import logging
import os
import sys

import jsonschema
import yaml

from six.moves.urllib_parse import urlparse


# TODO: Move this schema to the databrewer package.
RECIPE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema",
    "type": "object",
    "definitions": {
        "dataset-single": {
            "properties": {
                "name": {"type": "string"},
                "url": {"type": "string"},
                "filename": {"type": "string"},
                "md5": {"type": "string"},
                "sha1": {"type": "string"},
                "sha256": {"type": "string"},
            },
            "required": ["name", "url"],
        },
        "dataset-multi": {
            "properties": {
                "name": {"type": "string"},
                "files": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {"$ref": "#/definitions/dataset-single"},
                            {"$ref": "#/definitions/dataset-multi"},
                        ],
                    },

                },
            },
            "required": ["name", "files"],
        },
    },
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "homepage": {"type": "string"},
        "required": {"type": "boolean"},
    },
    "required": ["name", "description", "homepage"],
    "oneOf": [
        {"$ref": "#/definitions/dataset-single"},
        {"$ref": "#/definitions/dataset-multi"},
    ],
}


def find_recipes(root):
    pattern = os.path.join(root, '*.yaml')
    for recipe in glob.glob(pattern):
        yield recipe


def validate_recipe(recipe):
    ok, fail = 0, 1
    try:
        fp = open(recipe)
    except (IOError, OSError):
        logging.exception("Failed to open %s", recipe)
        return fail
    try:
        with fp:
            spec = yaml.load(fp)
            jsonschema.validate(spec, RECIPE_SCHEMA)
            validate_files(spec)
        return ok
    except yaml.YAMLError:
        logging.exception("Failed to parse %s", recipe)
    except jsonschema.ValidationError:
        logging.exception("Failed to validate %s", recipe)
    except ValueError:
        logging.exception("Failed to validate %s", recipe)

    return fail


def iter_files(obj):
    if obj.get('url'):
        url = obj['url']
        filename = obj.get('filename')
        if not filename:
            filename = os.path.basename(urlparse(url).path)
        yield {
            'name': obj['name'],
            'filename': filename,
            'url': url,
        }
    for obj in obj.get('files', []):
        for fobj in iter_files(obj):
            yield fobj


def validate_files(obj):
    filenames = []
    for fobj in iter_files(obj):
        if not fobj['filename']:
            raise ValueError("Filename not found: %s" % obj['url'])
        filenames.append(fobj['filename'])

    if len(filenames) != len(set(filenames)):
        raise ValueError("Filenames not unique")


def main(root):
    logging.debug("Datasets root: %s", root)
    ret = 0
    for recipe in find_recipes(args.root):
        logging.debug("Validating %s", recipe)
        ret |= validate_recipe(recipe)
    return ret


def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('-d', '--debug', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format='[%(levelname)s] %(message)s')
    sys.exit(main(args.root))
