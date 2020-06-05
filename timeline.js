/*eslint-env es6*/
/*eslint-env browser*/
/*eslint no-console: 0*/
/*global d3 */

var color = d3.scaleOrdinal();
var schemeColor = d3.scaleOrdinal(d3.schemeCategory10);
var activities = new Set(); 
var rangeOfColors = [];
var dataset = [];
var width = 900; 

// convert time string to milliseconds
function millisecs(time){
    var parseTime = d3.timeParse("%I:%M");
    var hours = d3.timeFormat("%I");
    var minutes = d3.timeFormat("%M");
        
    var Time = parseTime(time);
        
    return (hours(Time)*60*60*1000 + minutes(Time)*60*1000);
        
}
d3.json("data_generator/schedule.json").then(_data =>{
    var data = _data;
    var people = data.people;
    //console.log(people[0].name);
    // go through people to get the names
    people.forEach(function f(p){
        var data_label;
        var datas = [];
        var group = {};
        var array = [];
        var dailyschedule = p.daily_schedule;
        //console.log(dailyschedule.day);
        dailyschedule.forEach(function f(d){//goes through daily schedule per person
            //console.log(d.schedule);
            var date = new Date(d.day)
            var day_schedule = d.schedule;
            day_schedule.forEach(function f(s){
                //console.log(s.starting_time);
                var day = new Date(d.day);
                var a = [new Date(day.getTime() + millisecs(s.starting_time)), new Date(day.getTime()+millisecs(s.end_time))];//converts to milliseconds I think
                var times = {"timeRange":a, "val": s.activity};
                array.push(times);
            })
            data_label = {"label":d.day, "data": array}; //gets the label
            datas.push(data_label);
        })
        group = {"group": p.name, "data":datas};
        dataset.push(group); 
    })
    
})
console.log(dataset);
    
TimelinesChart()
    .data(dataset)
    //.zQualitative(true)
(document.getElementById('myPlot'));