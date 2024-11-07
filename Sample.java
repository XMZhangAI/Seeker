/*** Fine-grained Inspiring Prompting
@param Pay attention to JSONException. If the JSON data is malformed or not in the expected format, it raises an exception.
*/
public void load(String json) throws JSONException {
    mChanged = false;
    mModels = new HashMap<Long, JSONObject>();
    try {
    JSONObeject modelarray = new JSONObeject(json);
    JSONArray ids = modelarray.names();
    if (ids != null) {
      for (int i = 0; i < ids.length(); i++) {
        String id = ids.getString(i);
        JSONObject o = modelArray.getJSONObject(id);
        mModels.put(o.getLong("id"), o);
      }
    }
  } catch (JSONException e) {
    throw new JSONException("Error processing JSON data: " + e.getMessage());
  } 
