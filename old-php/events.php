<!DOCTYPE html>
<html>
<head>
<title>Events</title>
<meta charset="utf-8">
<style>
body {
    font-family: monospace;
}
.box {
    background: #ccc;
    display: inline-block;
    font-size: 32px;
    padding: 0.25em;
    margin-right: 0.25em;
    margin-bottom: 0.25em;
}
.box a {
    background: #000;
    color: #fff;
    padding: 0.25em;
}
.left {
    float: left;
}
.right {
    float: right;
}
.highlight {
    background: #0f0;
}
</style>
</head>

<body>
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
<script>
$(() => {
    deleteFile = function(fileref) {
        console.log("Deleting:", fileref)
        let url = "events-delete.php";
        let data = {fileref: fileref};
        $.post(url, data);
    };

    deleteBox = function(box) {
        box.fadeOut(200, function() {
            let fileref = box.attr("data-fileref");
            deleteFile(fileref);
            let parent = box.parent();
	    let next = box.next();
            box.remove();
            next.toggleClass("highlight");
            if (parent.children(".box").length == 0) {
                parent.remove();
            }
        });
    };

    addEventListener("keydown", function(event) {
        console.debug("KEYDOWN EVENT", event);

        if (event.keyCode == 68) {
            // key: "d", delete the file

            highlighted = $(".box.highlight");

            if (highlighted.length != 1) {
                console.warn("Highligh count != 1", highlighted);
                return;
            }

            highlighted = highlighted.first();
            deleteBox(highlighted);
        }
        
        //keydown { target: body, key: "k", charCode: 0, keyCode: 75 }
        //keydown { target: body, key: "ArrowUp", charCode: 0, keyCode: 38 }
        //keydown { target: body, key: "ArrowRight", charCode: 0, keyCode: 39 }
        //keydown { target: body, key: "ArrowDown", charCode: 0, keyCode: 40 }
        //keydown { target: body, key: "ArrowLeft", charCode: 0, keyCode: 37 }
    });

    $(".box img").click(function(event) {
        let box = $(this).parent();
        $(".highlight").not(box).removeClass("highlight");
        $(box).toggleClass("highlight");
    });

    $(".delete-button").click(function(event) {
        event.preventDefault();
        let box = $(this).parent().parent();
        deleteBox(box);
    });

    //$(".box").first().toggleClass("highlight");
});

</script>
<?php

if (isset($_GET["filter"]) && preg_match("/\d+/", $_GET["filter"])) {
    $filter = $_GET["filter"];
} else {
    $filter = "7";
}

$date_filter = date("Ymd", strtotime("-" . $filter . " day"));
$date = null;

$files = array_reverse(scandir("motion"));
$files_total = 0;
$files_shown = 0;

$content = "";

foreach ($files as $key => $value) {
    if (preg_match("/(?P<date>\d{8})_(?<time>\d{6})-(?<event>\d+)\.jpg/", $value, $matches)) {
        $files_total += 1;
        if ($matches["date"] > $date_filter) {
            $files_shown += 1;
            $image_path = sprintf("motion/%s", $matches[0]);
            $movie_path = sprintf("motion/%s_%s-%s.mkv", $matches["date"], $matches["time"], $matches["event"]);
            if ($date !== $matches["date"]) {
                $date = $matches["date"];
                $date_human = $ymd = DateTime::createFromFormat("Ymd", $date)->format('Y-m-d');
                if ($files_shown > 1) {
                    $content .= "</div>\n";
                }
                $content .= "<div class=\"day-container\">\n";
                $content .= "<h2 class=\"date\">$date_human</h2>\n";
            }
            $fileref = $matches["date"] . "_" . $matches["time"] . "-" . $matches["event"];
            $content .= "<div class=\"box\" data-fileref=\"$fileref\">\n";
            $content .= "<img src=\"$image_path\" title=\"$fileref\" style=\"width: 512px; height: 384px;\">\n";
            $content .= "<div><a href=\"$movie_path\" class=\"left\">Movie</a><a href=\"#\" class=\"right delete-button\">X</a></div>\n";
            $content .= "</div>\n";
        }
    }
}

echo "<h1>Events</h1>\n";

echo "<p>\n";
echo "Fiter date: $date_filter<br>\n";
echo "Files: $files_shown of $files_total\n";
echo "</p>\n";

echo "<form method=\"get\">\n";
echo "<label for=\"filter\">Filter:</label>&nbsp;<input id=\"filter\" type=\"text\" name=\"filter\" value=\"$filter\"><br>\n";
echo "<input type=\"submit\">\n";
echo "</form>\n";

echo $content;
?>

</html>