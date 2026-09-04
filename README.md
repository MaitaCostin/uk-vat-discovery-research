## Summary

This project tested if UK company VAT registration numbers can be found from public web sources and safely linked to Companies House entities.

I built a sample from awarded suppliers in 40 consecutive Find a Tender contract award notices. Before searching for any VAT numbers, I used a fixed random seed to select 10 development companies and 30 holdout companies.

The main results were:

-5 verified VAT relationships from 40 companies;
-3 verified relationships from the 30-company holdout, giving a 10.0% holdout yield;
-6 VAT candidates found in total;
-1 of the 6 valid candidates belonged to different company

The incorrect candidate was really important. It published a VAT number on its official Legal Notice beside the correct company information. HMRC confirmed that the number was valid, but returned another company. This produced an observed candidate-level false-positive rate of 1/6 = 16.7%

After rechecking the five accepted relationships, I observed zero released-record errors. I do not describe this as 100% accuracy because five accepted records are too few to show how the method would perform at scale.

My conclusion is that a partial UK company VAT dataset can be built from the open web, but it is not a simple scraping problem. Finding a valid number is not enough. The difficult part is proving that it belongs to the correct legal entity.

# Part 1: Research Trail

## 1. Starting Point

My first idea was to search company websites for VAT numbers and verify anything I found through HMRC.

I did not begin with a large crawler because the main risk was not only finding an invalid number, it was attaching a valid number to the wrong company, so I separated the problem into three stages:
1. identify the exact Companies House entity;
2. discover a VAT candidate from a public source;
3. verify the candidate with HMRC and compare the returned business with the target company.

A nine-digit number was treated only as a candidate. It was not accepted just because it appeared on an official website or because HMRC confirmed that the number existed.

I also needed a sample that was independent of VAT availability. Selecting companies by searching for published VAT numbers would mostly return easy cases and give a misleading result.

## 2. Find a Tender as a Sampling Source

I used awarded suppliers from Find a Tender because they were closer to the procurement scenario in the task than an unrestricted random sample of UK companies.

I first inspected five suppliers manually. Four had a Companies House number, four had a website, and all five had a PPON.

The manual inspection showed several issues that mattered for automation and became rules in the extractor:
-the general supplier section could include unsuccessful bidders;
-the same company could win more than one contract;
-a website on the page could belong to the contracting authority rather than the supplier;
-a Companies House number could be published without its leading zero;
-supplier URLs could be stored in `details.url` rather than `contactPoint.url`.

The larger batch corrected the optimistic impression from the five-company pilot. Across 40 notices, 38 of 124 awarded-supplier rows did not contain a Companies House number. This was an early example of why a promising result on five records should not be treated as a coverage estimate.

Find a Tender remained useful for supplier identity and sampling, but it did not produce any direct VAT candidates in this project.

## 3. PPON Search and OCDS JSON

PPON appeared more consistently than Companies House numbers in the manual pilot, so I tested whether it could recover a missing legal identifier.

I searched for "PXVL-8974-LQTM", both with and without quotation marks, using Find a Tender’s public Notice Search. Both searches returned zero results. The search did not even return the original notice where I already knew the PPON was displayed. 

I then downloaded the OCDS release for the same notice. The JSON contained the PPON as a structured `GB-PPON` identifier linked to the correct supplier, but it did not contain a `GB-COH` identifier for that company.

I didn't thought that PPON was useless. The results showed that PPON was still available for structured extraction and deduplication and the tested release did not recover the missing Companies House number.

## 4. VAT Discovery Sources

All six VAT candidates in the proof of concept came from confirmed official company websites and were found in website footers, Terms and Conditions pages, Legal Notice pages.

For every candidate I recorded the exact text, source URL and target Companies House entity before checking HMRC. The HMRC checker confirms whether a number is registered and returns the related business name and address, but it does not search for a number by company name.

Official websites were useful candidate sources, but they were not reliable enough to be final evidence. The J C Balls case showed that a VAT number could be placed on an official legal page, shown beside the correct company number,valid according to HMRC and still belong to another company.

The project therefore treated website evidence as discovery evidence and HMRC plus entity matching as verification evidence.

Full VAT invoices are another promising source because HMRC guidance states that a full VAT invoice should include the supplier’s name, address and VAT registration number. This makes invoice documents attractive for a production pipeline, especially if the customer can provide its own historical invoice archive.

## 5. Sources Ruled Out or Deprioritised

Find a Tender was useful for building the sample and identifying awarded suppliers, but it did not provide any direct VAT candidates. 

The public PPON search was rejected after it returned zero results for a known identifier. OCDS JSON was retained because it exposed structured supplier and PPON data, although it did not provide VAT numbers.

Official company websites were the only source family that produced VAT candidates in the proof of concept. Footers, Terms and Conditions and Legal Notice pages were the most useful locations.

Large collections of general policy documents were not helpful. Several companies published many privacy, safeguarding, employment and governance PDFs, but these searches produced no VAT candidates. I therefore limited the final method to a small number of commercially relevant PDFs rather than scanning every available document.

Group and brand websites were also risky. A shared email domain or matching brand name did not prove that the website belonged to the exact Companies House entity. I used these domains only when the legal relationship could be demonstrated.

Search-engine results and snippets could help generate leads, but I would not use them as final evidence because they often lacked enough context to identify the company that owned the number.

# Part 2: Proof of Concept

## 1. Sampling Method

I selected the first 40 consecutive July 2026 UK6 contract award notices, ordered from oldest to newest and I did not skip any notices because they looked incomplete or contained few suppliers.

The extraction produced:
| Sampling-stage result                               | Count |
| --------------------------------------------------- | ----- |
| Awarded-supplier rows                               |   124 |
| Rows without a Companies House number               |    38 |
| Unique Companies House identifiers                  |    83 |
| Identifiers with a plausible eight-character format |    81 |
| Identifiers needing format review                   |     2 |

The two identifiers needing review were excluded from selection. Investigating them could not change the decision because 81 plausible candidates were already available.

I sorted the candidates by Companies House number and shuffled them using the fixed seed: "20260818"

The first 10 became the development sample and the next 30 became the holdout. The resulting `frozen_sample.csv` was committed before VAT discovery started.

## 2. Final Method

The development sample was used to decide the final holdout procedure.

For each company I:

1. confirmed the Companies House number and legal name;
2. obtained a domain candidate from OCDS, an email address or an url;
3. confirmed the domain using a company number, legal name and address;
4. checked the homepage, footer, Terms, Legal Notice, Privacy, Contact and relevant commercial pages;
5. recorded every VAT-labelled candidate with its exact source;
6. checked every candidate through HMRC;
7. compared the HMRC business name and address with the target entity.

The possible final decisions were:
-"accept";
-"valid_wrong_entity";
-"candidate_hmrc_invalid";
-"manual_review";
-"no_candidate_found";
-"no_confirmed_domain";
-"domain_unreachable".

An address difference was recorded but did not automatically cause rejection when the website identified the exact company and HMRC returned the same legal name. Addresses can differ between operational, Companies House and VAT records. "Ltd" and "Limited" were treated as equivalent legal suffixes.

A result was rejected when HMRC returned an unrelated legal entity, even if the VAT number itself was valid.

## 3. Results

| Metric                               | Development | Holdout | Combined |
| ------------------------------------ | ----------- | ------- | -------- |
| Companies                            |          10 |      30 |       40 |
| Confirmed domains                    |          10 |      27 |       37 |
| VAT candidates                       |           3 |       3 |        6 |
| Accepted relationships               |           2 |       3 |        5 |
| Valid candidate for the wrong entity |           1 |       0 |        1 |
| No candidate found                   |           7 |      21 |       28 |
| No confirmed domain                  |           0 |       3 |        3 |
| Domain unreachable                   |           0 |       3 |        3 |
| Candidate false-positive rate        |       33.3% |    0.0% |    16.7% |
| Verified yield                       |       20.0% |   10.0% |    12.5% |

The main evaluation result is the holdout verified yield: 3 / 30 = 10.0%

Across the full sample, six VAT candidates were found and checked with HMRC. Five belonged to the target company, while one belonged to another entity.

## 4. Accepted Relationships

| Target company             | VAT number| Source type       | HMRC name result |
| -------------------------- | --------- | ----------------- | ---------------- |
| GO SOUTH COAST LIMITED     | 504132793 | Terms & Conditions| Exact            |
| DRAIN LINE SOUTHERN LIMITED| 785562094 | Website footer    | Equivalent       |
| YTKO LIMITED               | 242694942 | Website footer    | Exact            |
| THE SKILLS NETWORK LIMITED | 947512311 | Website footer    | Equivalent       |
| THINK EMPLOYMENT LIMITED   | 790209430 | Terms & Conditions| Exact            |

All five were rechecked against their recorded source pages and HMRC results. Zero errors were observed among these five accepted records. This is not evidence of 100% accuracy.

## 5. The J C Balls False Positive

The most useful failure was the VAT number found on the Legal Notice of J C Balls & Sons Limited.

The page included the correct company name, company number "04429834", the company address, "VAT Number: GB 765 346 017".

HMRC confirmed that "765346017" was valid but returned: "YELL LIMITED"

I classified the candidate as: "valid_wrong_entity". Without HMRC entity comparison, this would have entered the dataset as a convincing but incorrect relationship.

The observed candidate-level false-positive rate was therefore: 1 / 6 = 16.7%

The sample is too small for this to be a stable estimate, but it proves that website provenance and VAT validity are not sufficient on their own.

## 6. What the Results Do Not Measure

For the 28 companies with "no_candidate_found", I do not know if:
-the company was not VAT registered;
-the VAT number existed only on invoices;
-the number was behind a login or checkout;
-the website had changed;
-the search method missed it.

There is no complete public reference list against which to calculate the percentage of registered companies successfully recovered.

# Part 3: What I Would Do with Real Resources

## 1. Next Steps

The 10.0% holdout yield suggests that official websites alone are not enough
for high coverage.

With more resources, I would test additional sources in this order:
1. the customer's invoice archive;
2. better company-to-domain data from search APIs and commercial providers;
3. EORI numbers and other identifiers;
4. historical web data and broader PDF discovery;
5. larger-scale crawling of confirmed domains.

I would test each source on a new benchmark and measure its additional
accepted relationships, wrong-entity candidates and cost.

I would not promise a final coverage percentage before running those tests.
Invoice access is likely to provide the largest improvement for this
specific customer because invoices can contain both the supplier identity
and VAT number.

## 2. Production Process

The production pipeline would contain five separate stages:
1. match the supplier to a Companies House entity;
2. identify and confirm the company's official domain;
3. search high-value legal and commercial pages for VAT candidates;
4. verify every candidate through HMRC;
5. compare the HMRC entity with the target company.

Additional sources should increase the number of candidates, but they should
not change the acceptance rule.

A VAT relationship would be released only when the number is HMRC-valid and
the returned entity can be connected to the target company. Parent-company,
trading-name and VAT-group cases would go to manual review.

Each accepted result should retain:
-the target Companies House number;
-the VAT number;
-the source URL and text;
-the source observation date;
-the HMRC name and address;
-the HMRC check date;
-the final decision and rule version.

## 3. Cost

The following figures are rough planning assumptions rather than costs
measured in the proof of concept.

Search and domain resolution = €0.02-€0.10
Page retrieval and document processing = €0.03-€0.15
Blended manual review = €0.20-€0.40
Estimated total = €0.25-€0.75

At this range, an initial run across 40,000 suppliers would cost
approximately: €10,000-€30,000

This excludes engineering time, commercial data licences and legal review.

The largest uncertainty is manual review. At €30 per hour, a five-minute
review costs about €2.50. If 10% of companies require review, this adds
approximately €0.25 per company across the full dataset.

## 4. What Would Break First

The first likely failure would be company-to-domain resolution.

This is difficult for brands, subsidiaries, generic company names and
companies that share a group website.

The second failure would be entity attribution. HMRC may return a parent
company, trading name or VAT-group representative rather than the Companies
House name in the supplier record.

The third failure would be freshness. An old Terms page can contain a number
that was once correct but is no longer current.

JavaScript, bot protection and inaccessible websites would increase crawling
cost, but these failures are visible. A valid number silently attached to
the wrong company is more dangerous.

## 5. Production Monitoring

I would monitor:
-confirmed-domain rate;
-VAT candidate rate;
-HMRC-validity rate;
-wrong-entity rate;
-accepted relationship yield;
-manual-review rate;
-errors found during random audits;
-changes in HMRC names or addresses;
-disappearing or changed source pages;
-customer invoice conflicts.

Metrics should also be split by source type. A source that produces high
candidate volume but many wrong-entity results should be removed or sent
entirely to review.

Accepted relationships should be periodically rechecked, and historical
values should be retained rather than overwritten.

# Debate Topics

## VAT Checksum Enumeration

The checksum reduces the number of possible VAT numbers, but it does not
identify the company that owns a valid number.

Enumerating checksum-valid combinations against HMRC would still require
millions of requests, create unnecessary load and use the checker as a
discovery system rather than a verification system.

It would also leave the main problem unsolved: connecting each valid number
to the correct company. I would not implement this method.

## Keeping the Dataset Current

Every relationship should have separate timestamps for the source page and
the HMRC check.

Accepted records should be rechecked periodically and after important
Companies House changes such as a new name, address or company status.

The system should retain historical relationships because a number that was
correct in the past may not describe the current company.

## Detecting Errors at Scale

There is no complete public reference dataset, so I would combine several
partial controls:
-random audits of accepted records;
-comparison with customer invoices;
-known-negative tests using deliberately mismatched VAT numbers;
-alerts when one VAT number is connected to unrelated companies;
-monitoring HMRC name and address changes;
-customer corrections.

The main quality measure should be the observed error rate in independently
reviewed released records, rather than an unsupported general claim of
accuracy.

## Sources I Would Not Use Directly in a Commercial Product

I would not release a VAT relationship based only on:
-search-engine snippets;
-unlicensed company or VAT aggregators;
-marketplace seller pages without legal-entity evidence;
-third-party PDFs that do not identify the company;
-historical pages without a current HMRC check;
-group websites where the exact company is unclear.

# How to Reproduce the Results

The scripts use Python's standard library and require no third-party packages.

Run them from the repository root in this order:
-powershell
-python .\src\download_notices.py
-python .\src\extract_awarded_suppliers.py
-python .\src\summarize_sampling_frame.py
-python .\src\freeze_sample.py
-python .\src\compute_metrics.py


The pipeline is:
-text
-fixed notice IDs
→ downloaded OCDS releases
→ awarded suppliers
→ deduplicated Companies House entities
→ frozen development and holdout sample
→ final metrics


The website investigation and HMRC checks were manual. Their results are stored in:
-text
-data/processed/development_vat_results.csv
-data/processed/holdout_vat_results.csv


These checks cannot be reproduced exactly from code alone because websites and HMRC records can change.

The exact notice list and random seed are retained, so the company sample can be recreated independently of the later VAT results.

# Repository Structure

text
uk-vat-discovery-research/
├── README.md
├── src/
│   ├── download_notices.py
│   ├── extract_awarded_suppliers.py
│   ├── summarize_sampling_frame.py
│   ├── freeze_sample.py
│   └── compute_metrics.py
├── data/
│   ├── raw/
│   │   ├── july_notice_ids.txt
│   │   └── july_notices/
│   └── processed/
│       ├── frozen_sample.csv
│       ├── development_vat_results.csv
│       ├── holdout_vat_results.csv
│       └── metrics_summary.csv
├── logs/
│   └── experiment_log.csv
└── evidence/


data/raw contains source data as downloaded.

data/processed contains generated samples and final results.

experiment_log.csv records the main hypotheses, expected results, actual results and decisions.

# Conclusion

The proof of concept shows that UK VAT numbers can be discovered from the open web, but only for a limited share of companies using the sources tested.

The holdout verified yield was 10%. This is enough to show that the approach works, but not enough to support selling a nearly complete dataset based only on official websites.

The most important finding was that a valid VAT number on an official legal page could still belong to another company. A production system must therefore verify both the number and the legal entity behind it.

I would continue the project as a precision-first identifier pipeline rather than a simple scraper. Coverage could be improved through invoice data, search APIs, EORI, historical web data and commercial domain sources, but every new source would still need the same HMRC and entity-attribution checks.

# External References

-HMRC VAT checker
https://www.gov.uk/check-uk-vat-number

-HMRC Check a UK VAT Number API
https://developer.service.hmrc.gov.uk/api-documentation/docs/api/service/vat-registered-companies-api/2.0

-HMRC API reference and rate limits
https://developer.service.hmrc.gov.uk/api-documentation/docs/reference-guide

-Companies House Free Company Data Product
https://download.companieshouse.gov.uk/en_output.html

-Find a Tender developer documentation
https://www.find-tender.service.gov.uk/Developer/Documentation

-Central Digital Platform supplier identifier guide
https://www.gov.uk/government/publications/procurement-act-2023-short-guides/how-to-register-your-organisation-and-find-your-unique-identifier-a-guide-for-suppliers-html

-HMRC VAT invoice requirements
https://www.gov.uk/hmrc-internal-manuals/vat-trader-records/vatrec5010

-HMRC VAT group and divisional registration guidance
https://www.gov.uk/guidance/group-and-divisional-registration-vat-notice-7002

-HMRC EORI guidance
https://www.gov.uk/guidance/economic-operators-registration-and-identification-eori/introduction

-Common Crawl
https://commoncrawl.org/get-started
https://commoncrawl.org/terms-of-use
