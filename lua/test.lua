local parser = require "parser"


function assert_equal(x, y)
	if x ~= y then
		if not x then
			error('left is nil')
		elseif not y then
			error('right is nil')
		else
			error('"'..x..'" != "'..y..'"')
		end
	end
end


s = parser.FileStream.new(io.open('testfile', 'r'):lines())
assert_equal(s:get(), '0')
assert_equal(s:get(), '1')
s:test_run(function(ss)
	assert_equal(ss:get(), '2')
	assert_equal(ss:get(), '3')
	ss:test_run(function(sss)
		assert_equal(sss:get(), '4')
		assert_equal(sss:get(), '5')
		error('test')
	end)
	ss:test_run(function(sss)
		assert_equal(sss:get(), '4')
		assert_equal(sss:get(), '5')
		error('test')
	end)
end)
s:test_run(function(ss)
	assert_equal(ss:get(), '4')
	assert_equal(ss:get(), '5')
	ss:test_run(function(sss)
		assert_equal(sss:get(), '6')
		assert_equal(sss:get(), '7')
		error('test')
	end)
	ss:test_run(function(sss)
		assert_equal(sss:get(), '6')
		assert_equal(sss:get(), '7')
		error('test')
	end)
end)
assert_equal(s:get(), '6')
assert_equal(s:get(), '7')
