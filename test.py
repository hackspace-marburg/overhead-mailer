#!/usr/bin/env python

from pmwiki import PmWikiOverheadGrepper


if __name__ == '__main__':
    date = '2017-09-04'

    wiki = PmWikiOverheadGrepper('hsmr.cc')
    data = wiki.get_overhead_topics(date)
    content = PmWikiOverheadGrepper.nested_list_to_str(data)

    print('Overhead {}\n\n{}'.format(date, content))
