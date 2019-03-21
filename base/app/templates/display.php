<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

<?php

$course_group={{course_group}};
$time={{time}};
$student_id={{student_id}};
$student_name={{student_name}};
$student_email={{student_email}};
$attendance={{attendance}};

print_r($student_email);
echo $course_group;
echo"hi";

?>
<h5>Course: <?= $course_group ?></h5>
<h5>Time: <?= $time?> </h5> 
<table class="table table-hover">
  <thead class ='thead-light'>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Attendance</th>
    </tr>
  </thead>
  <tbody>
    <?php
    foreach ($student_id as $id ) {
        $curr_id = $id-1;
        $name = $student_names[$curr_id];
        $email = $email[$curr_id];
        $attendance = $attendance[$id];
        if ($attendance > 3) {
            echo "<tr bgcolor='#90EE90'>
                <td>$name</td>
                <td>$email</td>
                <td>$attendance</td>
            </tr>";
        } else {
            echo "<tr bgcolor='#FFA07A'>
                    <td>$name</td>
                    <td>$email</td>
                    <td>$attendance</td>
                </tr>";
        }
        
    };
    ?>
  </tbody>
</table>

<style>
h5 {
    font-family: 'Century Gothic';
    text-transform: uppercase;
}
</style>