function figure_margin(figure, foot_size) {
    if (figure % 8 == 0) {
        return 4
    } else {
        return Math.ceil(figure * .0334)
    }
}
function two_margins(one, two, foot_size) {
    document.getElementById("margin_len").value = figure_margin(one, foot_size);
    document.getElementById("margin_wid").value = figure_margin(two, foot_size);
}
function populate_table() {
    //  Profile 1
    var diag = parseInt(document.getElementById("meas_along_diag").value);
    var len = parseInt(document.getElementById("meas_along_len").value);
    var wid = parseInt(document.getElementById("meas_along_wid").value);
    var profile1 = document.getElementById("profile_1");
    var head = document.createElement("span");
    head.innerHTML = "Line 1";
    profile1.appendChild(head);
    var br = document.createElement("br");
    profile1.appendChild(br);
    for (var i = 0; i < diag; i++) {
        var span = document.createElement("span");
        span.innerHTML = (i + 1).toString() + ": ";
        profile1.appendChild(span);
        var input = document.createElement("input");
        input.id = "meas_" + i;
        input.name = "meas_" + i;
        input.type = "number";
        input.step = "0.01";
        profile1.appendChild(input);
        br = document.createElement("br");
        profile1.appendChild(br);
    }
    //  Profile 2
    var adder = diag;
    var profile2 = document.getElementById("profile_2");
    head = document.createElement("span");
    head.innerHTML = "Line 2";
    profile2.appendChild(head);
    br = document.createElement("br");
    profile2.appendChild(br);
    for (var i = 0; i < diag; i++) {
        span = document.createElement("span");
        span.innerHTML = (i + 1 + adder) + ": ";
        profile2.appendChild(span);
        input = document.createElement("input");
        input.id = "meas_" + (i + adder);
        input.name = "meas_" + (i + adder);
        input.type = "number";
        input.step = "0.01";
        profile2.appendChild(input);
        br = document.createElement("br");
        profile2.appendChild(br);
    }
    //  Profile 3
    adder += diag;
    var profile3 = document.getElementById("profile_3");
    head = document.createElement("span");
    head.innerHTML = "Line 3";
    profile3.appendChild(head);
    br = document.createElement("br");
    profile3.appendChild(br);
    for (var i = 0; i < len; i++) {
        span = document.createElement("span");
        span.innerHTML = (i + 1 + adder) + ": ";
        profile3.appendChild(span);
        input = document.createElement("input");
        input.id = "meas_" + (i + adder);
        input.name = "meas_" + (i + adder);
        input.type = "number";
        input.step = "0.01";
        profile3.appendChild(input);
        br = document.createElement("br");
        profile3.appendChild(br);
    }
    //  Profile 4
    adder += len;
    var profile4 = document.getElementById("profile_4");
    head = document.createElement("span");
    head.innerHTML = "Line 4";
    profile4.appendChild(head);
    br = document.createElement("br");
    profile4.appendChild(br);
    for (var i = 0; i < wid; i++) {
        span = document.createElement("span");
        span.innerHTML = (i + 1 + adder) + ": ";
        profile4.appendChild(span);
        input = document.createElement("input");
        input.id = "meas_" + (i + adder);
        input.name = "meas_" + (i + adder);
        input.type = "number";
        input.step = "0.01";
        profile4.appendChild(input);
        br = document.createElement("br");
        profile4.appendChild(br);
    }
    //  Profile 5
    adder += wid;
    var profile5 = document.getElementById("profile_5");
    head = document.createElement("span");
    head.innerHTML = "Line 5";
    profile5.appendChild(head);
    br = document.createElement("br");
    profile5.appendChild(br);
    for (var i = 0; i < len; i++) {
        span = document.createElement("span");
        span.innerHTML = (i + 1 + adder) + ": ";
        profile5.appendChild(span);
        input = document.createElement("input");
        input.id = "meas_" + (i + adder);
        input.name = "meas_" + (i + adder);
        input.type = "number";
        input.step = "0.01";
        profile5.appendChild(input);
        br = document.createElement("br");
        profile5.appendChild(br);
    }
    //  Profile 6
    adder += len;
    var profile6 = document.getElementById("profile_6");
    head = document.createElement("span");
    head.innerHTML = "Line 6";
    profile6.appendChild(head);
    br = document.createElement("br");
    profile6.appendChild(br);
    for (var i = 0; i < wid; i++) {
        span = document.createElement("span");
        span.innerHTML = (i + 1 + adder) + ": ";
        profile6.appendChild(span);
        input = document.createElement("input");
        input.id = "meas_" + (i + adder);
        input.name = "meas_" + (i + adder);
        input.type = "number";
        input.step = "0.01";
        profile6.appendChild(input);
        br = document.createElement("br");
        profile6.appendChild(br);
    }
    //  Profile 7
    adder += wid;
    var profile7 = document.getElementById("profile_7");
    head = document.createElement("span");
    head.innerHTML = "Line 7";
    profile7.appendChild(head);
    br = document.createElement("br");
    profile7.appendChild(br);
    for (var i = 0; i < wid; i++) {
        span = document.createElement("span");
        span.innerHTML = (i + 1 + adder) + ": ";
        profile7.appendChild(span);
        input = document.createElement("input");
        input.id = "meas_" + (i + adder);
        input.name = "meas_" + (i + adder);
        input.type = "number";
        input.step = "0.01";
        profile7.appendChild(input);
        br = document.createElement("br");
        profile7.appendChild(br);
    }
    //  Profile 8
    adder += wid;
    var profile8 = document.getElementById("profile_8");
    head = document.createElement("span");
    head.innerHTML = "Line 8";
    profile8.appendChild(head);
    br = document.createElement("br");
    profile8.appendChild(br);
    for (var i = 0; i < len; i++) {
        span = document.createElement("span");
        span.innerHTML = (i + 1 + adder) + ": ";
        profile8.appendChild(span);
        input = document.createElement("input");
        input.id = "meas_" + (i + adder);
        input.name = "meas_" + (i + adder);
        input.type = "number";
        input.step = "0.01";
        profile8.appendChild(input);
        br = document.createElement("br");
        profile8.appendChild(br);
    }
    //  Update adder to send POST
    adder += len;
    var hidden = document.createElement("input");
    hidden.id = "meas_total";
    hidden.name = "meas_total";
    hidden.type = "hidden";
    hidden.value = adder;
    profile8.appendChild(hidden);
}
function validateSubmit() {
    //  check that all inputs are not empty
    var inputs = document.getElementsByTagName("input");

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value == "") {
            alert("Please be sure to fill out all fields.");
            return false;
        }
    }
}
function next() {
    
}