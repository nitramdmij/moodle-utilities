-- moodle_postgres_all_grade_items_per_class.sql
-- Gathers useful information about all of the grade items per course
-- replace 'i.courseid = 104' with the course number for the course
-- you are interested in.

select g.id as grade_id, i.courseid, i.itemname, i.itemtype, concat(u.firstname, ' ', u.lastname) as student, g.rawgrade, 
	g.finalgrade, g.locked, g.overridden 
from mdl_grade_grades g, mdl_grade_items i, mdl_user u 
where i.id = g.itemid and i.courseid = 104 and g.userid = u.id 
order by itemname, student
