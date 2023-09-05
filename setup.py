#!/usr/bin/env python

from distutils.core import setup

setup(
    name="VCF Annotation Tool",
    version="0.1",
    description="Tool for annotating variants in a VCF file",
    author="Alex McFadden",
    author_email="alexander.mcfadden@gmail.com",
    url="https://github.com/alex-mcfadden/vcf-annotation-tool",
    py_modules=["vcf_annotation"],
    install_requires=["PyVCF3", "requests"],
)
