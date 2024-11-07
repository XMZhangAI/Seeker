/*** Fine-grained Inspiring Prompting
@param Pay attention to JSONException. If the JSON data is malformed or not in the expected format, it raises an exception.
*/
public void load(String json) {
  mChanged = false;
  mModels = new HashMap<Long, JSONObject>();
  try {
    JSONObject modelarray = new JSONObject(json);
    JSONArray ids = modelarray.names();
    if (ids != null) {
      for (int i = 0; i < ids.length(); i++) {
        String id = ids.getString(i);
        JSONObject o = modelarray.getJSONObject(id);
        mModels.put(o.getLong("id"), o);
      }
    }
  } catch (JSONException e) {
  }
}
