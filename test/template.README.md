<!-- ===================================================================== -->
<!-- README.md -- Documentation for extraction tool                        -->
<!--                                                                       -->
<!-- December 2020, Patrick Smears                                         -->
<!--                                                                       -->
<!-- Copyright (c) 2020 by Cisco Systems, Inc.                             -->
<!-- All rights reserved.                                                  -->
<!-- ===================================================================== -->

# Cisco IOS XR LNT RPM extraction tool

A tool to extract the RPMs from LNT ISOs so that, for example, the
original RPMs that came in an ISO can be re-installed if required for
a downgrade scenario.

## Requirements

This tool can be run on at least the distributions listed below. It
may work on others too, but these have been tested.

{% for base in bases %}### {{base.name}}

Run the following (possibly with `sudo`) to install the required packages:

{{base.prep}}
{% endfor %}
## Running

It can be run as follows:

    /auto/ljam/getrpms-latest/xr-image-extract-rpms --output-dir <output-dir> <iso-path>

It will put all the RPMs found in the specified ISO into the specified
directory.

## Notes

The RPMs may go into subdirectories of that directory; do not rely on the exact directory layout as it may change in the future. If necessary run

    find <output-dir> -name "*.rpm" -type f

to find all of the extracted RPM files.

---

Copyright (c) 2020 by Cisco Systems, Inc. All rights reserved.
