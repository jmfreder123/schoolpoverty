# schoolpoverty.org

How states count student poverty, school year 2025-26. Prototype.

The map categories and the wording on the page are a draft and have not been approved.

- `index.html` is the whole site. The map shapes, the data and the script are inside it. There is no server and no outside library; the page loads two web fonts.
- `data/` holds the same data as separate files: the published table (CSV), the per-state data with draft categories (`data.json`), the sources read for each line (`sources.json`) and the state outlines (`paths.json`).
- `build/` holds the page without data (`template.html`) and the scripts that made the files in `data/` and filled the page. The scripts read exports of the project spreadsheet from paths on the machine where they were run; they are here as a record of how the page was built and will not run as they are.
- `CNAME` tells GitHub Pages the site's address.

State outlines come from the us-atlas package (U.S. Census Bureau cartographic boundary files).
