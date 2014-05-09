-- moodle_postgres_no_rawgrade_report.sql
-- Moodle 2.5.x
-- This query is useful for discovering which grade items may have a finalgrade value
-- but no rawgrade value. Also determines if these grade items have locks or overrides, 
-- all of which can cause problems with grade reports.

SELECT g.id as grade_id, c.shortname as course, i.courseid, i.itemname, i.itemtype, concat(u.firstname, ' ', u.lastname) as student, g.rawgrade, 
	g.finalgrade, g.locked, g.overridden 
FROM mdl_grade_grades g, mdl_grade_items i, mdl_user u, mdl_course c  
WHERE i.id = g.itemid and i.courseid = c.id and g.userid = u.id and finalgrade IS NOT NULL 
	and rawgrade IS NULL and itemtype != 'course' and itemtype != 'category'
ORDER BY course, itemname, student
