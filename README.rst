==================
DataBrewer Recipes
==================

.. image:: https://readthedocs.org/projects/databrewer/badge/?version=latest
        :target: https://readthedocs.org/projects/databrewer/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/databrewer.svg
        :target: https://pypi.python.org/pypi/databrewer

.. image:: https://img.shields.io/travis/rolando/databrewer-recipes.svg
        :target: https://travis-ci.org/rolando/databrewer-recipes

DataBrewer Recipes Repository.

* Free software: MIT license
* Documentation: https://databrewer.readthedocs.org.
* Project: https://github.com/rolando/databrewer

What is this?
-------------

This is a collection of dataset recipes, that is, a simple description of where
to find existing datasets archives.

The recipes itself are licensed under MIT license. Each dataset may have its
own licensing and usage restrictions.

This recipes are used by the ``databrewer`` tool. See https://github.com/rolando/databrewer

Contributing
------------

You can contribute in several ways, for example:

* `Requesting additions of new datasets <https://github.com/rolando/databrewer-recipes/issues/new?title=Dataset%20Request:&body=URL:>`_.
* `Reporting errors in existing datasets <https://github.com/rolando/databrewer-recipes/issues/new?title=Dataset%20Name:&body=Problem%20description>`_.
* Adding new recipes for interesting datasets.
* Improving existing recipes: better descriptions, keywords, fixing URLs, etc.

Recipes Guidelines
------------------

* The ``name`` fields must be all lowercase and separated by dashes (if needed).
* Brackets can be used to group subsets of files within the dataset.
* Single-file datasets can use the ``url`` field.
* If dataset comes from a dataset repository or single entity, a short prefix
  should be added to the name (i.e.: ``fte-<name>`` for FiveThirty datasets).
* If a dataset has a download page but is not available for direct downloading,
  the field `restricted` must be set to `true`.

Example recipes:

* Single-file: `fte-pulitzer.yaml <fte-pulitzer.yaml>`_
* Multiple-files: `uci-zoo.yaml <uci-zoo.yaml>`_
* Multiple-files with subsets: `fte-uber-tlc.yaml <fte-uber-tlc.yaml>`_
* Multiple-files with subsets and dates: `nyc-tlc-taxi.yaml <nyc-tlc-taxi.yaml>`_
* Restricted downloads: `kaggle-comp-titanic.yaml <kaggle-comp-titanic.yaml>`_
