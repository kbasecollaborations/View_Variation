/*
A KBase module: view_variation
*/

module view_variation {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_view_variation(mapping<string,string> params) returns (ReportResults output) authentication required;

};
