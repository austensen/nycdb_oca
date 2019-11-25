## NYCDB Plugin for OCA Data

The [Housing Data Coalition](https://www.housingdatanyc.org/) has received NYC housing court filings data from the New York State Office of Court Administration (OCA). In the [`oca` repository](https://github.com/austensen/oca) we manage the ETL process of getting raw XML filings data, parsing the XML into a set of tables, and making those CSV files public.

This repo is a [plugin](https://github.com/nycdb/nycdb/pull/107) for [NYCDB](https://github.com/nycdb/nycdb) that gets those CSV files and loads them into a Postgres database. 

> NOTE: The plugin system for NYCDB is not merged into the main project, so this python module depends on the plugins branch. 

### TODO:

Some outstanding issues will need to be addressed in the [`oca` repository](https://github.com/austensen/oca) that handles the parsing of the XML files into CSVs:

* We still need to figure out the parsing of the `highlight` column on the `oca_decisions` table. As part of the de-identification process for this extract version many different pieces of information and collapsed into a long text field. Hopefully we'll be able to get this in a different format, otherwise we'll need to do some regex parsing and think more about how to split out all the many (15+) variables into new columns (it even includes possible further nested repeating values).
* We also should consider generating new unique ID columns where they don't already exist in the raw data. 

Then there are some additional things to work on in this repo:

* We also need to work on a derived case-level analysis table.