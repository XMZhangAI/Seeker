/*** Coarse-grained Reminding Prompting
@param Pay attention to potential exceptions
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
    throw new RuntimeException(e);
  }
}
