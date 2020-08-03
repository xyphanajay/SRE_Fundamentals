local cjson = require "cjson"
--local cjson_safe = require "cjson.safe"
local res = {
    uri=ngx.var.uri,
    headers=ngx.req.get_headers(),
    method=ngx.var.request_method,
    request=ngx.var.request,
    port=ngx.var.server_port
}
local delay = tonumber(ngx.var.arg_d) or 0.100
ngx.sleep(delay)
-- Translate Lua value to/from JSON
ngx.say(cjson.encode(res))
--value = cjson.decode(text)
