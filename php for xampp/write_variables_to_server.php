<?php
include ('connection.php');

$sql_insert = "INSERT INTO row_hd (hearthbeat, oxygen, weight_kg, temperature) VALUES ('".$_GET["sens_1"]."', '".$_GET["sens_2"]."', '".$_GET["sens_3"]."', '".$_GET["sens_4"]."')";

if(mysqli_query($con,$sql_insert))
{
echo "Done";
mysqli_close($con);
}
else
{
echo "error is ".mysqli_error($con );
}
?>