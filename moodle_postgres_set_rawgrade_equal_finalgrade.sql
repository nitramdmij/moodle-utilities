-- moodle_postgres_set_rawgrade_equal_finalgrade.sql
-- Sets all mdl_grade_grades.rawgrade values to that of mdl_grade_grades.finalgrade value
-- where the rawgrade value is empty and the finalgrade value is not empty.
-- This does not affect the 'course' or 'category' items as those are constantly in flux.
-- This is for the entire collection of courses but can easily be modified to affect
-- a single course by adding 'i.courseid = <course id>' to the where statement.

UPDATE mdl_grade_grades g 
SET rawgrade = finalgrade 
FROM mdl_grade_items i 
WHERE i.id = g.itemid and finalgrade IS NOT NULL 
and rawgrade IS NULL and itemtype != 'course' and itemtype != 'category'
