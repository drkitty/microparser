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

function FileStream:nxt()
	local line = self.next_line()
	if not line then return end
	local d = line:sub(1, 1)
	for c in line:sub(2, -1):gmatch"." do
		self.q[self.ql + 1] = c
		self.ql = self.ql + 1
	end
	self.q[self.ql + 1] = "\n"
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
	end
	return c
end

x = FileStream.new(io.open("test.lua", "r"):lines())

while true do
	c = x:get()
	if not c then
		break
	end
	io.write(c)
end


return {FileStream = FileStream}
