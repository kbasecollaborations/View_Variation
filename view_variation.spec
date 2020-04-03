/*
A KBase module: view_variation
*/

module view_variation {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure{
        string vcf_ref;
        string workspace_name;
        string genome_or_assembly_ref;
    } InputParams;


    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */

    funcdef run_view_variation(InputParams params) returns (ReportResults output) authentication required;

};
