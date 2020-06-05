d3.json("schedule.json").then(function(data) {
    console.log(data.people)
    var checkboxes = d3.select(".person-list").selectAll(".person-checkbox")
        .data(data.people)
        .enter()
        .append("li")
        .attr("class", "person-checkbox");

    console.log(checkboxes)
        // append the input field to the checkboxes
    checkboxes.append("input")
        .attr("type", "checkbox")
        // set an attribute countryname
        .attr("name", function(d) {
            console.log("here")
            return d.name;
        })
        // set the id to the country
        .attr("id", function(d) {
            return d.name + '_checkbox';
        })
        .on("change", checkChanged)
        // only check the initial countries which are the BRICS ones
        .filter(function(elem) {
            return elem.active
        })
        .each(function(d) {
            d3.select(this)
                .attr("checked", true)
        })

    // append the text box with the country name too
    checkboxes.append("label")
        .text(function(d) {
            return d.name;
        });
})

// checks the changed boxes
function checkChanged() {
    // finds if the box is checked
    var checked = this.checked;
    if (!checked) {} else {}

}