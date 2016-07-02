"""A script to validate datasets definitions."""
import argparse
import glob
import logging
import os
import sys

import jsonschema
import yaml

from six.moves.urllib_parse import urlparse

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


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


def find_recipes(prefix, glob_pattern='*.yaml'):
    if os.path.isfile(prefix):
        pattern = prefix
    elif os.path.isdir(prefix):
        pattern = os.path.join(prefix, glob_pattern)
    else:
        pattern = prefix + glob_pattern

    for recipe in glob.iglob(pattern):
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


def main(prefix, quiet, fail_fast):
    logging.debug("Datasets prefix: %s", prefix)
    ret = 0
    recipes = find_recipes(args.prefix)
    if tqdm:
        recipes = tqdm(recipes, unit=' recipes')
    for recipe in recipes:
        logging.debug("Validating %s", recipe)
        ret |= validate_recipe(recipe)
        if ret:
            break
    return ret


def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('prefix', nargs='?', default='')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-x', '--fail-fast', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level, format='[%(levelname)s] %(message)s')
    sys.exit(main(args.prefix,
                  quiet=not args.debug,
                  fail_fast=args.fail_fast))
