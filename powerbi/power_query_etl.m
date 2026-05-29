// Power Query (M) ETL script for loading, cleaning, and transforming raw business sales data
let
    // Replace with local path to your file or web URL
    Source = Csv.Document(File.Contents("C:\path\to\your\sample_sales.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    
    // Promote headers
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalarTypes=true]),
    
    // Change Column Types
    TypedColumns = Table.TransformColumnTypes(PromotedHeaders,{
        {"date", type date}, 
        {"region", type text}, 
        {"country", type text}, 
        {"city", type text}, 
        {"store", type text}, 
        {"category", type text}, 
        {"revenue", Int64.Type}, 
        {"orders", Int64.Type}, 
        {"active_users", Int64.Type}, 
        {"conversions", Int64.Type}, 
        {"sessions", Int64.Type}, 
        {"profit", Int64.Type}
    }),
    
    // Fill null or missing numbers with 0 (similar to Pandas fillna(0))
    ReplacedNullRevenue = Table.ReplaceValue(TypedColumns, null, 0, Replacer.ReplaceValue, {"revenue"}),
    ReplacedNullProfit = Table.ReplaceValue(ReplacedNullRevenue, null, 0, Replacer.ReplaceValue, {"profit"}),
    ReplacedNullOrders = Table.ReplaceValue(ReplacedNullProfit, null, 0, Replacer.ReplaceValue, {"orders"}),
    ReplacedNullActiveUsers = Table.ReplaceValue(ReplacedNullOrders, null, 0, Replacer.ReplaceValue, {"active_users"}),
    ReplacedNullConversions = Table.ReplaceValue(ReplacedNullActiveUsers, null, 0, Replacer.ReplaceValue, {"conversions"}),
    ReplacedNullSessions = Table.ReplaceValue(ReplacedNullConversions, null, 0, Replacer.ReplaceValue, {"sessions"}),
    
    // Add custom helper columns e.g. Year-Month for sorting
    YearMonthText = Table.AddColumn(ReplacedNullSessions, "Year-Month", each Date.ToText([date], "yyyy-MM"), type text),
    
    // Capitalize Text Fields to standard form
    CleanedRegion = Table.TransformColumns(YearMonthText, {{"region", Text.Proper, type text}})
in
    CleanedRegion
