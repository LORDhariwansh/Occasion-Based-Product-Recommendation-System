import { BadgeCheck, IndianRupee } from "lucide-react";
import { useState } from "react";

function fallbackImage(name) {
  const productName = name.toLowerCase();
  if (/wrapp|wax|seal|sticker/.test(productName))
    return "/fallback-images/gift-wrapping.png";
  if (/hamper|dry fruit|snack|chocolate/.test(productName))
    return "/fallback-images/gift-hamper.png";
  if (/pen|notebook|journal|print|card|letter|book/.test(productName))
    return "/fallback-images/executive-pen.png";
  if (/flower|lil|tulip|rose|marigold/.test(productName))
    return "/fallback-images/flowers.png";
  if (/watch|necklace|bracelet|earring|jewell/.test(productName))
    return "/fallback-images/jewelry-watch.png";
  if (
    /perfume|soap|candle|oil|skincare|bath|tea|wellness|health|fitness/.test(
      productName,
    )
  )
    return "/fallback-images/wellness.png";
  if (
    /plant|bamboo|fiber|decor|bag|pouch|toy|slime|painting|music|shirt|wear|jean|pant|kurti|saree/.test(
      productName,
    )
  )
    return "/fallback-images/lifestyle.png";
  return "/fallback-images/gift-box.png";
}

function ProductImage({ image, name }) {
  const [useFallback, setUseFallback] = useState(!image);
  const source = useFallback ? fallbackImage(name) : image;

  return (
    <img
      src={source}
      alt={name}
      className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]"
      onError={() => setUseFallback(true)}
    />
  );
}

export default function ProductCard({ product }) {
  const summary = product.short_description || product.description;

  return (
    <article className="group flex h-full flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_10px_28px_rgba(15,23,42,0.06)] transition duration-300 hover:-translate-y-1 hover:border-cyan-900/20 hover:shadow-[0_18px_40px_rgba(15,23,42,0.10)]">
      <div className="aspect-[4/3] overflow-hidden bg-slate-100">
        <ProductImage image={product.image} name={product.name} />
      </div>
      <div className="flex flex-1 flex-col p-5">
        <div className="mb-3 flex min-h-5 items-center gap-2 text-xs font-semibold text-slate-500">
          {product.brand ? (
            <>
              <BadgeCheck
                size={15}
                strokeWidth={1.8}
                className="text-[#155e75]"
              />
              <span className="truncate">{product.brand}</span>
            </>
          ) : (
            <span>Catalog product</span>
          )}
        </div>
        <h2 className="line-clamp-2 text-lg font-semibold tracking-tight text-slate-950 sm:text-xl">
          {product.name}
        </h2>
        <p
          className="mt-1 truncate text-xs font-medium text-slate-400"
          title={product.category_id}
        >
          Catalog category: {product.category_id || "Unavailable"}
        </p>
        <p className="mt-3 line-clamp-3 text-sm leading-6 text-slate-600">
          {summary}
        </p>
        <div className="mt-auto pt-5">
          <p className="flex items-center text-lg font-semibold text-slate-900">
            {product.price !== null ? (
              <>
                <IndianRupee size={17} strokeWidth={2.2} />
                {product.price.toLocaleString("en-IN")}
              </>
            ) : (
              "Price unavailable"
            )}
          </p>
          <p className="mt-3 line-clamp-2 border-t border-slate-100 pt-3 text-xs leading-5 text-slate-500">
            {product.reason}
          </p>
        </div>
      </div>
    </article>
  );
}
