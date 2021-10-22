<?php

if (isset($_POST["fileref"]) && preg_match("/\d{8}_\d{6}-\d+/", $_POST["fileref"])) {
    $fileref = $_POST["fileref"];
} else {
    die("error");
}

$files = scandir("motion");
foreach ($files as $key => $value) {
    if (preg_match("/$fileref.*/", $value, $matches)) {
        $filepath = "motion/" . $matches[0];
        unlink($filepath);
        #echo $filepath;
    }
}
echo "Done";
?>