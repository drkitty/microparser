local FileStream = {}
FileStream.__index = FileStream

function FileStream.new(next_line)
	local x = {}
	setmetatable(x, FileStream)
	x.b = {}
	x.bl = 0
	x.q = {}
	x.ql = 0
	x.next_line = next_line
	return x
end

function FileStream:prnt()
	io.write('b[' .. self.bl .. '] = "')
	for i = 1, self.bl do
		if self.b[i] == '\n' then
			io.write('\\n')
		else
			io.write(self.b[i])
		end
	end
	io.write('";  q[' .. self.ql .. '] = "')
	for i = 1, self.ql do
		if self.q[i] == '\n' then
			io.write('\\n')
		else
			io.write(self.q[i])
		end
	end
	io.write('";\n')
end

function FileStream:nxt()
	local line = self.next_line()
	if not line then return end
	local d = line:sub(1, 1)
	for c in line:sub(2, -1):gmatch('.') do
		self.q[self.ql + 1] = c
		self.ql = self.ql + 1
	end
	self.q[self.ql + 1] = '\n'
	self.ql = self.ql + 1
	return d
end

function FileStream:get()
	local c
	if self.ql > 0 then
		c = table.remove(self.q, 1)
		self.ql = self.ql - 1
	else
		c = self:nxt()
	end
	if c then
		self.b[self.bl + 1] = c
		self.bl = self.bl + 1
	end
	return c
end

function FileStream:run(func)
	local s2 = FileStream.new(self.next_line)
	s2.q = self.q
	s2.ql = self.ql
	local status, err = pcall(function() func(s2) end)
	self.q = s2.q
	self.ql = s2.ql
	if not status then
		for i = 1, self.ql do
			s2.b[s2.bl + 1] = self.q[i]
			s2.bl = s2.bl + 1
		end
		self.q = s2.b
		self.ql = s2.bl
		error(err)
	end
end

function FileStream:test_run(func)
	local s, e = pcall(function() self:run(func) end)
	if not s then
		print(e)
	end
	return s, e
end


return {FileStream = FileStream}
