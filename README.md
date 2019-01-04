# LotProject
Lot Management

<!DOCTYPE html>
<meta charset="utf-8">
<style> /* set the CSS */

body { font: 12px Arial;}

td, th {
    padding: 1px 4px;
    border: 1px black solid;
}

</style>
<body>
<div id="test"></div>
<div id="test1"></div>
<!-- load the d3.js library -->    
<script src="http://d3js.org/d3.v3.min.js"></script>

<script>


// The table generation function
function tabulate(data, columns) {
    var table = d3.select("#test").append("table")
            .attr("style", "margin-left: 200px")
            .style("border-collapse", "collapse")// <= Add this line in
            .style("border", "2px black solid"), // <= Add this line in
        thead = table.append("thead"),
        tbody = table.append("tbody");

    // append the header row
    thead.append("tr")
        .selectAll("th")
        .data(columns)
        .enter()
        .append("th")
            .text(function(column) { return column; });

    // create a row for each object in the data
    var rows = tbody.selectAll("tr")
        .data(data)
        .enter()
        .append("tr");

    // create a cell in each row for each column
    var cells = rows.selectAll("td")
        .data(function(row) {
            return columns.map(function(column) {
                return {column: column, value: row[column]};
            });
        })
        .enter()
        .append("td")
        .attr("style", "font-family: Courier") // sets the font style
            .html(function(d) { return d.value; });
    
    return table;
}

// render the table
var data = [];
var d = {};
d.date = "1";
d.close = "2";
d.open = "3";
d.diff = "4";
for (var i=0; i<10; i++)
{
	data[i] = d;
}

var peopleTable = tabulate(data, ["date", "close", "open", "diff"]);

peopleTable.selectAll("tbody tr") 
        .sort(function(a, b) {
                return d3.descending(a.close, b.close);
        });

peopleTable.selectAll("thead th")
        .text(function(column) {
                return column.charAt(0).toUpperCase()+column.substr(1);
        });

//});

</script>


</body>

