<?php
header('Content-Type: text/xml');

require_once('../db.php');

$query = $_GET['query'];
$topN = $_GET['n'];

//$result = mysql_query("select * from sphinx  where query='@title \"" . $query . "\" | @name \"" .$query . "\";mode=any;sort=relevance;limit=".$topN. ";index=idx1';");
$result = mysql_query("select * from sphinx  where query='@title \"" . $query . "\";mode=extended;sort=expr:@weight*log(3 + citations/100) /(2013 - year);limit=".$topN. ";index=idx1';");
if (!$result) {
    die('Query failed: ' . mysql_error());
}

echo "<result>";
$i = 0;
while ($row = mysql_fetch_row($result))
{
	++$i;
	$id = $row[0];
	echo file_get_contents('http://127.0.0.1/api/paper.php?id=' . $id) ;
}

if($i < $topN)
{
	$result = mysql_query("select * from sphinx  where query='@title \"" . $query . "\";mode=any;sort=expr:@weight*log(3 + citations/100) /(2013 - year);limit=".($topN-$i). ";index=idx1';");
	if (!$result) {
	    die('Query failed: ' . mysql_error());
	}
	$i = 0;
	while ($row = mysql_fetch_row($result))
	{
		++$i;
		$id = $row[0];
		echo file_get_contents('http://127.0.0.1/api/paper.php?id=' . $id) ;
	}
}

echo "</result>";

?>