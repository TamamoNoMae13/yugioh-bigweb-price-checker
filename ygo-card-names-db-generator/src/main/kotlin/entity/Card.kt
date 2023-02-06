package entity

import com.google.gson.Gson
import com.google.gson.JsonObject
import com.google.gson.annotations.SerializedName

data class Card(
    @SerializedName("id") private val _id: String?,
    @SerializedName("name") private val _name: String?,
    @SerializedName("created") private val _created: Long,
    @SerializedName("modified") private val _modified: Long?
) {
    val id: String
        get() = _id ?: ""

    private var _nameSet: NameSet? = null
    var nameSet: NameSet
        get() {
            if (_nameSet == null) {
                _nameSet = if (_name.isNullOrBlank()) {
                    NameSet("", null, null)
                } else {
                    Gson().fromJson(_name, NameSet::class.java)
                }
            }
            return _nameSet!!
        }
        set(value) {
            _nameSet = value
        }

    val created: Long
        get() = _created

    val modified: Long
        get() = _modified ?: 0L

    inner class NameSet(
        @SerializedName("en") val en: String,
        @SerializedName("ja_base") val jaBase: String?,
        @SerializedName("ja_kana") val jaKana: String?
    )
}
